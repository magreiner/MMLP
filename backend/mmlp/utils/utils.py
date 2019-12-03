import datetime
import falcon
import json
import logging
import math
import os
import re
import smtplib
import tarfile
import time
import zipfile
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mmlp.Config import Config


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


def get_all_files_with_ending(path, ending):
    results = []

    for file in os.listdir(path):
        if file.endswith(ending):
            results += [os.path.join(path, file)]

    #     os.chdir(path)
    #     for file in glob.glob(ending):
    #         results += [file]
    #
    return results


def remove_nan_from_dict(dictionary):
    for item in dictionary:
        if isinstance(dictionary[item], dict):
            remove_nan_from_dict(dictionary[item])
        if isinstance(dictionary[item], float):
            if math.isnan(dictionary[item]):
                dictionary[item] = "undefined"

    return dictionary


# Extract the name of the repository, e.g.:
# source_url = "git@github.com:some_user/MMLP"
# repo_name = "MMLP"
def extract_repository_name(source_url):
    repo_name_pattern = r"([a-zA-Z\\-\\_\\.]{1,})$"
    repo_name_prog = re.compile(repo_name_pattern)

    _, repo_name, _ = repo_name_prog.split(source_url)

    return repo_name.replace(".git", "")


def get_metadata_from_directories(base_dir, meta_file_name, ignore_directories=None):
    if ignore_directories is None:
        ignore_directories = ["lost+found", ".vscode", ".idea"]

    result = []
    for current_dir in os.listdir(base_dir):
        # Ignore files and system or custom directories
        if not os.path.isdir(os.path.join(base_dir, current_dir)) or current_dir in ignore_directories:
            continue

        meta_file_path = os.path.join(base_dir, current_dir, meta_file_name)
        if os.path.exists(meta_file_path):
            with open(meta_file_path, 'rb') as f:
                result_entry = json.load(f)
        else:
            result_entry = 'No metadata available'

        result += [result_entry]

    return result


def throw_exception(name, description):
    logger = logging.getLogger('backend.' + name)
    logger.error("name: {}, desc: {}".format(name, description))
    raise falcon.HTTPServiceUnavailable(
        "How boring to be in a predictable world. Here some surprise - just for you :)",
        "name: {}, desc: {}".format(name, description),
        30)


def get_timestamp(date_format="Default"):
    # Return a filename-friendly format
    if date_format == "filename":
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    elif date_format == "Default":
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    else:
        # Logging
        logger = logging.getLogger('backend.' + __name__)
        logger.fatal("Unknown date_format {}.".format(date_format))


def remove_ansi_escape_tags(string):
    tags = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    return tags.sub('', string)


def send_email_config(config: Config, subject: str, body: str, attachments=None):
    return send_email(to_address=config.email_notification_to,
                      smtp_address=config.email_notification_smtp_address,
                      username=config.email_notification_username,
                      password=config.email_notification_password,
                      subject=subject,
                      body=body,
                      from_address=config.email_notification_from,
                      attachments=attachments)


def send_email(to_address, smtp_address, username, password, subject, body, from_address, attachments=None):
    # Logging
    logger = logging.getLogger('backend.' + __name__)
    logger.info("Sending Email to {}, Subject: {}".format(to_address, subject))

    # Authenticate
    server = smtplib.SMTP_SSL(smtp_address, 465)
    server.ehlo()
    server.login(username, password)

    # Compose Email
    message = MIMEMultipart("mixed")
    message["Subject"] = f" [MMLP - Notification]: {subject}"
    message["From"] = from_address
    message["Return-Path"] = from_address
    message["To"] = to_address
    message.attach(MIMEText(body, "plain", _charset="utf-8"))

    for attach in attachments:
        part = MIMEText(attach["Content"], _subtype="x-log", _charset="utf-8")
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attach['Filename']}",
        )
        message.attach(part)

    # Send Email
    server.sendmail(from_address, to_address, message.as_string())

    # Logout
    server.quit()


def read_json_file(filename):
    # Logging
    logger = logging.getLogger('backend.' + __name__)

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            json_meta_data = json.load(f)

        return json_meta_data
    else:
        logger.fatal("The path to the file '{}' is invalid!".format(filename))

        return False


def write_to_file(file, content, mode="w"):
    with open(file, mode) as text_file:
        text_file.write(content)


def write_json_file(filename, content, mode="w"):
    with open(filename, mode) as outfile:
        json.dump(content, outfile)

    return True


def update_json_file(json_file_path, key, value):
    # Read current metadata
    json_meta_data = read_json_file(json_file_path)

    # Update dictionary
    json_meta_data[key] = value

    # Store updated metadata
    write_json_file(json_file_path, json_meta_data)

    return True


# def commonprefix(l):
#     # Based on:
#     # https://stackoverflow.com/questions/21498939/how-to-circumvent-the-fallacy-of-pythons-os-path-commonprefix
#     # Written by: Dan D., 1. Feb .2014
#     # this unlike the os.path.commonprefix version
#     # always returns path prefixes as it compares
#     # path component wise
#     cp = []
#     ls = [p.split(os.path.sep) for p in l]
#     ml = min(len(p) for p in ls)
#
#     for i in range(ml):
#
#         s = set(p[i] for p in ls)
#         if len(s) != 1:
#             break
#
#         cp.append(s.pop())
#
#     return '/'.join(cp)


def zip_directory(path, zip_handle, files_to_ignore=None):
    # Ensure trailing / (important for "removing" the common path in zip)
    if files_to_ignore is None:
        files_to_ignore = []

    if not path.endswith("/"):
        path = path + "/"

    # Add all files to zip
    for root, dirs, files in os.walk(path):
        for file in files:
            if file not in files_to_ignore:
                file_path = os.path.join(root, file)
                zip_handle.write(file_path, file_path.replace(path, ""))


def create_directory_zip(path, name):
    # Create zipfile
    new_zipfile = zipfile.ZipFile('{}.zip'.format(os.path.join(path, name)), 'w', zipfile.ZIP_DEFLATED)

    # Add contents
    zip_directory(path=path,
                  zip_handle=new_zipfile,
                  files_to_ignore=["{}.zip".format(name)])

    # Close file
    new_zipfile.close()

    return True


def create_directory_tar(path, name):
    # Create tarfile
    # w:gz to compress
    new_tarfile = tarfile.open('{}.tar'.format(os.path.join(path, name)), 'w')

    # Add contents
    for f in os.listdir(path):
        new_tarfile.add(f)

    # Close file
    new_tarfile.close()

    return True
