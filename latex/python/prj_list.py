#use python -u prj_list.py | tee prj.csv

import time,re
import subprocess
from pathlib import Path
from PICSimLab_rcontrol import PICSimLab_rcontrol
import shutil

def run_picsimlab(board="", processor="", fname=""):
    exe_path = r"/usr/bin/picsimlab"
    #exe_path = r"/home/gamboa/projetos/picsimlab/src/picsimlab"
    if len(board)  > 0: 
        if len(processor) > 0:
            if len(fname) > 0:
                file_path = Path(fname)
                if not file_path.is_file():
                    raise  print(f"File not found {file_path}")
                return subprocess.Popen([exe_path, board, processor, str(file_path)], stdout=subprocess.DEVNULL)
            else:
                return subprocess.Popen([exe_path, board, processor], stdout=subprocess.DEVNULL)     
        else:
            return subprocess.Popen([exe_path, board], stdout=subprocess.DEVNULL)
    else:
        return subprocess.Popen(exe_path, stdout=subprocess.DEVNULL)
  
process= run_picsimlab()
time.sleep(2) 
print("Board,Processor,IDE,Framework,Code Template")
try:
    with PICSimLab_rcontrol(5000) as rc:
        rc.cmd_blist()
        line = rc.get_cmd_response().splitlines()[1]
        #line="Arduino_Mega,Curiosity,ESP32_C3_DevKitC_02,Franzininho_DIY"
        boards = [item.strip() for item in line.split(",") if item.strip()]
        rc.cmd_exit()
        process.wait()
        #dir_path = Path("/tmp/prjwizard/")
        #shutil.rmtree(dir_path, ignore_errors=True)
        #dir_path.mkdir(parents=True, exist_ok=True)

    for board in boards:
        #print(f"## {board}")
        process= run_picsimlab(board)
        time.sleep(2) 
        with PICSimLab_rcontrol(5000) as rc:
            rc.cmd_spshow(0)
            rc.cmd_oscshow(0)
            rc.cmd_buclist()
            line = rc.get_cmd_response().splitlines()[1]
            processors = [item.strip() for item in line.split(",") if item.strip()]

            rc.cmd_bilist()
            line=rc.get_cmd_response().splitlines()[1]
            ides = [item.strip() for item in line.split(",") if item.strip()]
            if(ides[0] == "N/A"):
                processors=[] 
                print(f"{board},{processor},{ide},N/A,N/A")
                #print("-  This board hasn't supported IDEs !")
            
            rc.cmd_exit(1)
            process.wait()

            for processor in processors:
                #print(f"### {processor}")
                process= run_picsimlab(board, processor)
                time.sleep(2)         
                rc = PICSimLab_rcontrol(5000) 
                try:
                    do_exit = 1
                    rc.cmd_bilist()
                    line=rc.get_cmd_response().splitlines()[1]
                    ides = [item.strip() for item in line.split(",") if item.strip()]
                    for ide in ides:
                        rc.cmd_pwflist(ide)
                        line=rc.get_cmd_response().splitlines()[1]
                        frameworks = [item.strip() for item in line.split(",") if item.strip()]
                        for framework in frameworks:
                            rc.cmd_pwtlist(ide, framework)
                            line=rc.get_cmd_response().splitlines()[1]
                            templates = [item.strip() for item in line.split(",") if item.strip()]
                            for template in templates:
                                if template != "N/A":
                                    print(f"{board},{processor},{ide},{framework},{template}")
                                    #fname = f"{dir_path}/{board}_{processor}_{ide}_{framework}_{template}.pzw"
                                    #fname = fname.replace(" ", "_")
                                    pname = f"/tmp/{processor}_{template}"
                                    pname = pname.replace(" ", "_")
                                    #print(fname)
                                    #print(pname)

                                    #if do_exit :
                                        #Path(fname).unlink(missing_ok=True)
                                        #rc.cmd_saveworkspace(fname)

                                    #shutil.rmtree(pname, ignore_errors=True)
                                else:   
                                    print(f"{board},{processor},{ide},{framework},{template}")
                                    #print("-  This processor hasn't supported code templates !")
                    if do_exit :
                        rc.cmd_exit()
                        process.wait()

                finally:
                    rc.close()
                        
except ConnectionError as e:
    print(f"ConnectionError: {e}")

