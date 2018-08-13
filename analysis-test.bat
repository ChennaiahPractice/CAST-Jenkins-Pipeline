@echo off

set profile=webstore
set app=Webstore
set packageTemplate=Baseline
set snapshotName=%date:~-4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2% 

echo -- Packaging and Delivery of Source Code --
call .\\CLI-Scripts\\CMS_AutomateDelivery.bat "profile=%profile%" "app=%app%" "fromVersion=%packageTemplate%" "version=%snapshotName%"

echo -- Analyze Application --
call %WORKSPACE%\\CLI-Scripts\\CMS_Analyze.bat "profile=%profile%" "app=%app%"

echo -- Generate Snapshot --
call %WORKSPACE%\\CLI-Scripts\\CMS_GenerateSnapshot.bat "profile=%profile%" "app=%app%" "version=%snapshotName%"
