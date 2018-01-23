#!/usr/bin/python
import argparse
import jenkins
from os import listdir, path
import shutil

# Args parse
parser = argparse.ArgumentParser(description='Purge Jenkins job\'s builds')
parser.add_argument('--server', help='Jenkins server')
args = parser.parse_args()

# In case of you have multiple Jenkins servers
jenkinsServers = {
    'your_jenkins_server': {
        'url': 'http://your_jenkins_server:8080',
        'username': 'admin',
        'password': 'p@ssw0rd',
        'jobs_directory': '/var/lib/jenkins/jobs'
    }
}

# Jenkins server selected
jenkins_server = jenkinsServers[args.server]

# Connect to Jenkins server
server = jenkins.Jenkins(jenkins_server['url'], username=jenkins_server['username'], password=jenkins_server['password'])

# Get all jobs from Jenkins using API
jobs = server.get_all_jobs()

for job in jobs:
    # It's better to use a simple variable name
    job_name = job['name']

    # Get number of last job's build
    lastBuildNumber = server.get_job_info(job_name)['lastBuild']['number']

    # Job's builds directory
    job_builds_directory = "{}/{}/builds".format(jenkins_server['jobs_directory'], job_name)

    # Here is the trick
    for build_directory in listdir(job_builds_directory):
        if build_directory.isdigit() and int(build_directory) in range(1, lastBuildNumber-10):
            build_directory_path = path.join(job_builds_directory, build_directory)
            print "Deleting: " + build_directory_path
            shutil.rmtree(build_directory_path)
