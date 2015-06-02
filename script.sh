#!/bin/bash
echo "Starting Data Collection"
echo "Infected Image: "$1 " --- Baseline: " $2 " --- Options: " $3
/Users/Lunde/Downloads/volatility_2.4.mac.standalone/./volatility_2.4_x64 --plugins=/Users/Lunde/volatility_plugins/ -f /Users/Lunde/Desktop/VMs/Windows\ XP\ Professional.vmwarevm/Windows\ XP\ Professional-Snapshot$1.vmem --profile=WinXPSP3x86 ariel &&
/Users/Lunde/Downloads/volatility_2.4.mac.standalone/./volatility_2.4_x64 --plugins=/Users/Lunde/volatility_plugins/ -f /Users/Lunde/Desktop/VMs/Windows\ XP\ Professional.vmwarevm/Windows\ XP\ Professional-Snapshot$1.vmem --profile=WinXPSP3x86 regcheck &&
/Users/Lunde/Downloads/volatility_2.4.mac.standalone/./volatility_2.4_x64 --plugins=/Users/Lunde/volatility_plugins/ -f /Users/Lunde/Desktop/VMs/Windows\ XP\ Professional.vmwarevm/Windows\ XP\ Professional-Snapshot$1.vmem --profile=WinXPSP3x86 servicecheck &&
/Users/Lunde/Downloads/volatility_2.4.mac.standalone/./volatility_2.4_x64 --plugins=/Users/Lunde/volatility_plugins/ -f /Users/Lunde/Desktop/VMs/Windows\ XP\ Professional.vmwarevm/Windows\ XP\ Professional-Snapshot$1.vmem --profile=WinXPSP3x86 drivercheck &&
echo "Data Collection Complete!"
while true; do
    read -p "Compare the data?" yn
    case $yn in
        [Yy]* ) (	python dllCompare.py Windows%20XP%20Professional-Snapshot$2.vmem_DLL_List.p Windows%20XP%20Professional-Snapshot$1.vmem_DLL_List.p $3 && 
        			python runKeyCompare.py Windows%20XP%20Professional-Snapshot$2.vmem_RegKeyList.p Windows%20XP%20Professional-Snapshot$1.vmem_RegKeyList.p &&
        			python serviceCompare.py Windows%20XP%20Professional-Snapshot$2.vmem_ServiceList.p Windows%20XP%20Professional-Snapshot$1.vmem_ServiceList.p &&
        			python driverCompare.py Windows%20XP%20Professional-Snapshot$2.vmem_DriverList.p Windows%20XP%20Professional-Snapshot$1.vmem_DriverList.p &&
        			echo ""
                    echo "Comparison complete"
        			); break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
