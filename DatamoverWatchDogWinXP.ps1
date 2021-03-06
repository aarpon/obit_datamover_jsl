# Datamover Watch Dog
# PowerShell script
#
# Copyright, Aaron Ponti, 2014 - 2015
#
# Add this as a scheduled task in Windows to check for the status of the Datamover service and
# restart it in case it is not running. Make sure that the script is run by a user that has 
# enough rights to start services. This scripts logs to the Application event log with source
# oBITDatamoverWatchDog.
#
# For Windows XP, install PowerShell 1.0 (requires DotNet > 2.0):
#   http://www.microsoft.com/en-US/download/details.aspx?id=9591
#   http://go.microsoft.com/fwlink/?linkid=57014&lcid=0x409
#   http://www.microsoft.com/en-za/download/details.aspx?id=25

# Service name
$serviceName = "Datamover"

# Get the Datamover service
$service = Get-Service -Name $serviceName -ErrorVariable getServiceError -ErrorAction SilentlyContinue

# Is the service running?
if ($getServiceError)
{
    Write-Error "The $serviceName service does not appear to exist!"
    Exit
}

# Check the status and start the service is currently not running
if ($service.Status -ne "running") {
    Start-Service $serviceName
} else {
    Write-Host "The $serviceName service is running."
}
