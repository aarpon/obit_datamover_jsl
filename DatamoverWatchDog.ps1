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
# For Windows XP, use DatamoverWatchDogWinXP.ps1 instead!

# Service name
$serviceName = "Datamover"

# Event log name
$logSource = "oBITDatamoverWatchDog"

# We write to the Application event log, which should always exist. To be safe, we test for its
# existence and create it in case it does not exist.
$appLogExists = [System.Diagnostics.EventLog]::Exists('Application')
$sourceExists = [System.Diagnostics.EventLog]::SourceExists($logSource) 
if (! $appLogExists -or ! $sourceExists) {
    New-EventLog -LogName Application -Source $logSource
}

# Get the Datamover service
$service = Get-Service -Name $serviceName -ErrorVariable getServiceError -ErrorAction SilentlyContinue

# Is the service running?
if ($getServiceError)
{
    Write-EventLog -LogName "Application" -Source $logSource -EventId 0 -EntryType Error -Message "The $serviceName service does not appear to exist!"
    Exit
}

# Check the status and start the service is currently not running
if ($service.Status -ne "running") {
    Start-Service $serviceName
    Write-EventLog -LogName "Application" -Source $logSource -EventId 1 -EntryType Information -Message "Started $serviceName service."
}
