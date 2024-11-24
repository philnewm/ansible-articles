Automated installation
* https://www.sidefx.com/faq/question/install-linux/
* https://www.sidefx.com/docs/houdini/licensing/script_houdini_installations.html#script_houdini_install
* `INSTALL` file in extracted installer directory
* --accept-EULA required date to know which EULA will be accepted (ATTOW "2021-10-13")
* Bunch of dependencies missing
* SELinux prevents service startup by default  
* SELinux pretty strict by default - research why  
* SELinux set to enforcing by default  
* Setting to permissive works but security issue  
* Permissive mode will also spam warnings  
* Also huge security risk - like disabling anti virus?  
* Register sesinted (license service) with SELinux to allow  
* Only necessary for local license manager - like apprentice license on Linux  
* Test for AppArmor in Ubuntu  
* Houdini setup stopped working in Virtualbox from version 19 onward, check why

## Automated Downloads

* https://www.sidefx.com/docs/api/download/index.html#api-usage-example
* 