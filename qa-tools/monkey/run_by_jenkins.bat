@echo off
set /p job_name=job name?(transsnet_master, transsnet_develop...)
set /p must_stable=only run stable build?(y/n)
if "%must_stable%"=="y" (
    py run_by_jenkins.py %job_name% 
) else (
    py run_by_jenkins.py %job_name% 10000 nostable
)
