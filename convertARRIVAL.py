import pandas as pd
import datetime as dt
import numpy as np
import os
from localfunction import *
from pathlib import Path
import datetime
from datetime import datetime as dt

# function
def change_trigger(bool_d, name):
    bool_d = bool_d.fromkeys(bool_d,False)
    bool_d[name] = True
    return(bool_d)

def cdate(param):
    return(dt.strptime(param,"%Y-%m-%d"))

def ctime(param):
    return(dt.strptime(param,"%H:%M:%S.%f"))
    
# import path and data
path = "G:/My Drive/Tomography/121223/"
arrival_fname = "arrivals-cile.txt"
station_fname = "etc/indonesia_station.txt"
output_type = "pha" #stead (STEAD Dataset CSV) or pha (hypodd-phase)

# check if output files with name exist:
if os.path.isfile(path+Path(arrival_fname).stem+".csv") and output_type == "stead":
    print(f"output file exist! \nplease delete {path+Path(arrival_fname).stem+'.csv'}")
    exit()
    # return print("aborting!")
elif os.path.isfile(path+Path(arrival_fname).stem+".dat") and output_type == "pha":
    print(f"output file exist! \nplease delete {path+Path(arrival_fname).stem+'.dat'}")
    exit()
    # return print("aborting!")

# read station
sta_dict = pd.read_csv(station_fname, sep="\t",names=['station','lat','lon','elevation']).set_index('station').to_dict('index')

# define dataframe columns for STEAD format
if output_type == "stead":
    # adding s_travel_sec 
    columns_ = ['network_code',
                'receiver_code',
                'receiver_type',
                'receiver_latitude',
                'receiver_longitude',
                'receiver_elevation_m',
                'p_arrival_sample',
                'p_status',
                'p_weight',
                'p_travel_sec',
                's_arrival_sample',
                's_status',
                's_weight',
                's_travel_sec',
                'source_id',
                'date_',
                'source_origin_time',
                'source_origin_uncertainty_sec',
                'source_latitude',
                'source_longitude',
                'source_error_sec',
                'source_gap_deg',
                'source_horizontal_uncertainty_km',
                'source_depth_km',
                'source_depth_uncertainty_km',
                'source_magnitude',
                'source_magnitude_type',
                'source_magnitude_author',
                'source_mechanism_strike_dip_rake',
                'source_distance_deg',
                'source_distance_km',
                'back_azimuth_deg',
                'snr_db',
                'coda_end_sample',
                'trace_start_time',
                'trace_category',
                'trace_name']
    df = pd.DataFrame(columns= columns_)
    df.to_csv(path+Path(arrival_fname).stem+".csv",mode='a', header=True, index=False)
# define outputfile for pha format
elif output_type == "pha":
    df = pd.DataFrame(columns= [
                    'flag',
                    'year',
                    'month',
                    'day',
                    'hour',
                    'minutes',
                    'seconds',
                    'latitude',
                    'longitude',
                    'depth',
                    'magnitude',
                    'horizontal_error',
                    'depth_error',
                    'RMS',
                    'ID',])
else:
    print(f"output file format not supported --> {output_type}")
    exit()
    
# start read and convert
# initiate trigger bool and trigger counter
trigger_d = {
    "event" : False,
    "origin" : False,
    "netmag" : False,
    "phase" : False,
    "stamag" : False,
    }
trigger_counter = 0
event_counter = 1

# run
fin = open(path+arrival_fname,'r')
lines = fin.readlines()
for i, line in enumerate(lines):
    # skip header
    if "for 1 event:" in line.lower():
        continue
    # accomodate missing pick
    if "missing pick" in line.lower() or "##" in line.lower():
        continue
    # init trigger
    if "event:" in line.lower():
        trigger_d = change_trigger(trigger_d,"event")
        # print(f"event in line {i}")
        trigger_counter += 1
    elif "origin:" in line.lower():
        trigger_d = change_trigger(trigger_d,"origin")
        # print(f"origin in line {i}")
        trigger_counter += 1
    elif "network magnitudes:" in line.lower():
        trigger_d = change_trigger(trigger_d,"netmag")
        # print(f"network magnitudes in line {i}")
        trigger_counter += 1
    elif "phase arrivals:" in line.lower():
        trigger_d = change_trigger(trigger_d,"phase")
        # print(f"phase arrivals in line {i}")
        trigger_counter += 1
    elif "station magnitudes:" in line.lower():
        trigger_d = change_trigger(trigger_d,"stamag")
        # print(f"station magnitudes in line {i}")
        trigger_counter += 1
    else:
        pass
    
    # event block reading
    if "public id" in line.lower() and trigger_d['event']:
        eventid_ = line.split()[2]
    
    # origin block reading
    if trigger_d['origin']:
        if ("date" in line.lower()):
            date_ = cdate(line.split()[1])
        elif ("time" in line.lower()) and ("creation" not in line.lower()):
            time_uncertainty_sec_ = line.split()[-2]
            time_ = ctime(line.split()[1])
            datetime_ = dt.combine(date_.date(),time_.time())
        elif "latitude" in line.lower():
            lat_ = line.split()[1]
            lat_uncertainty_km_ = line.split()[-2]
        elif "longitude" in line.lower():
            lon_ = line.split()[1]
            lon_uncertainty_km_ = line.split()[-2]
        elif "depth" in line.lower():
            depth_ = line.split()[1]
            if "fixed" in line.lower():
                depth_uncertainty_km_ = 0
            else:
                depth_uncertainty_km_ = line.split()[4]
        elif "azimuthal gap" in line.lower():
            azgap_ = line.split()[2]
        elif "residual rms" in line.lower():
            source_error_sec_ = line.split()[-2]
        elif "author" in line.lower():
            author_ = line.split()[-1]
        elif "mode" in line.lower():
            mode_ = line.split()[-1]
        elif 'lat_uncertainty_km_' and 'lon_uncertainty_km_' in globals():
            source_horizontal_uncertainty_km_ = max(lat_uncertainty_km_,lon_uncertainty_km_)
        else:
            pass
    
    # network magnitude block reading
    if trigger_d['netmag']:
        if "preferred" in line.lower():
            source_mag_ = line.split()[1]
            source_mag_type_ = line.split()[0]
    
    # phase arrival block reading + writing output format
    if trigger_d['phase']:
        if len(line.split()) > 3 and "sta" in line.lower() and output_type == "pha":
            #pha header write
            phaheader_ = {
                    'flag'                 :   ["#"], ### done ###
                    'year'                 :   [date_.year], ### done ###
                    'month'                :   [date_.month], ### done ###
                    'day'                  :   [date_.day], ### done ###
                    'hour'                 :   [time_.hour], ### done ###
                    'minutes'              :   [time_.minute], ### done ###
                    'seconds'              :   [time_.strftime("%S.%f")], ### done ###
                    'latitude'             :   [lat_], ### done ###
                    'longitude'            :   [lon_], ### done ###
                    'depth'                :   [depth_], ### done ###
                    'magnitude'            :   [source_mag_], ### done ###
                    'horizontal_error'     :   [source_horizontal_uncertainty_km_], ### done ###
                    'depth_error'          :   [depth_uncertainty_km_], ### done ###
                    'RMS'                  :   [source_error_sec_], ### done ###
                    'ID'                   :   [event_counter], ### done ###
                    }
            df = pd.concat([df,pd.DataFrame(phaheader_)])
            
        elif len(line.split()) > 3 and "sta" not in line.lower():
            net_ = line.split()[1]
            sta_ = line.split()[0]
            receiver_type_ = "BH" # default 
            source_dist_deg_ = line.split()[2]
            source_dist_km_ = float(source_dist_deg_) * 111.11
            azimuth_ = line.split()[3]
            
            # station info
            if sta_ in sta_dict:
                lat_sta_ = float(sta_dict[sta_]['lat'])
                lon_sta_ = float(sta_dict[sta_]['lon'])
                elev_sta_ = float(sta_dict[sta_]['elevation'])
            else: # if station is not available in station data 
                lat_sta_ = None
                lon_sta_ = None
                elev_sta_ = None
            
            # phase info
            pha = line.split()[4]
            if pha == 'P':
                p_arrival_sample_ = line.split()[5]
                p_weight_ = line.split()[-2]
                p_travel_sec_ = abs(ctime(p_arrival_sample_) - time_).total_seconds()
                p_status_ = mode_
                s_arrival_sample_ = None
                s_weight_ = None
                s_travel_sec_ = None
                s_status_ = None
                tt_pha = p_travel_sec_
            elif pha == 'S':
                p_arrival_sample_ = None
                p_weight_ = None
                p_travel_sec_ = None
                p_status_ = None
                s_arrival_sample_ = line.split()[5]
                s_weight_ = line.split()[-2]
                s_travel_sec_ = abs(ctime(s_arrival_sample_) - time_).total_seconds()
                s_status_ = mode_
                tt_pha = s_travel_sec_
            else:
                p_arrival_sample_ = None
                p_weight_ = None
                p_travel_sec_ = None
                p_status_ = None
                s_arrival_sample_ = None
                s_weight_ = None
                s_travel_sec_ = None
                s_status_ = None
                tt_pha = None
            
            # save data stead
            if output_type == "stead":
                data_ = {
                    'network_code'                  :   [net_], ### done ###
                    'receiver_code'                 :   [sta_], ### done ###
                    'receiver_type'                 :   [receiver_type_], ### done ###
                    'receiver_latitude'             :   [lat_sta_], ### done ###
                    'receiver_longitude'            :   [lon_sta_], ### done ###
                    'receiver_elevation_m'          :   [elev_sta_], ### done ###
                    'p_arrival_sample'              :   [p_arrival_sample_], ### done ###
                    'p_status'                      :   [p_status_], ### done ###
                    'p_weight'                      :   [p_weight_], ### done ###
                    'p_travel_sec'                  :   [p_travel_sec_], ### done ###
                    's_arrival_sample'              :   [s_arrival_sample_], ### done ###
                    's_status'                      :   [s_status_], ### done ###
                    's_weight'                      :   [s_weight_], ### done ###
                    's_travel_sec'                  :   [p_travel_sec_], ### done ###
                    'source_id'                     :   [eventid_], ### done ###
                    'date_'                         :   [date_.strftime("%d/%m/%Y")], ### done ###
                    'source_origin_time'            :   [datetime_.strftime("%d/%m/%Y %H:%M:%S.%f")], ### done ###
                    'source_origin_uncertainty_sec' :   [time_uncertainty_sec_], ### done ###
                    'source_latitude'               :   [lat_], ### done ###
                    'source_longitude'              :   [lon_], ### done ###
                    'source_error_sec'              :   [source_error_sec_], ### done ###
                    'source_gap_deg'                :   [azgap_], ### done ###
                    'source_horizontal_uncertainty_km': [source_horizontal_uncertainty_km_], ### done ###
                    'source_depth_km'               :   [depth_], ### done ###
                    'source_depth_uncertainty_km'   :   [depth_uncertainty_km_], ### done ###
                    'source_magnitude'              :   [source_mag_], ### done ###
                    'source_magnitude_type'         :   [source_mag_type_], ### done ###
                    'source_magnitude_author'       :   [author_], ### done ###
                    'source_mechanism_strike_dip_rake': ['None'],
                    'source_distance_deg'           :   [source_dist_deg_], ### done ###
                    'source_distance_km'            :   [source_dist_km_], ### done ###
                    'back_azimuth_deg'              :   [azimuth_],
                    'snr_db'                        :   ['None'],
                    'coda_end_sample'               :   ['None'],
                    'trace_start_time'              :   ['None'],
                    'trace_category'                :   ['None'],
                    'trace_name'                    :   ['None']
                    }
                df = pd.concat([df,pd.DataFrame(data_)])
            
            # save data pha  
            elif output_type == "pha":
                phadata_ = {
                    'flag'                 :   [sta_], ### changing data to STA ###
                    'year'                 :   [tt_pha], ### changing data to TT ###
                    'month'                :   ['1'], ### changing data to WEIGHT ### # default value #
                    'day'                  :   [pha], ### changing data to PHA TYPE ###
                    'hour'                 :   [None], ### changing data to None After this ###
                    'minutes'              :   [None], 
                    'seconds'              :   [None], 
                    'latitude'             :   [None], 
                    'longitude'            :   [None], 
                    'depth'                :   [None],
                    'magnitude'            :   [None],
                    'horizontal_error'     :   [None], 
                    'depth_error'          :   [None], 
                    'RMS'                  :   [None], 
                    'ID'                   :   [None], 
                    }
                df = pd.concat([df,pd.DataFrame(phadata_)])
        else:
            pass
        
    # data saving
    if trigger_counter == 5:
        #save data stead
        if output_type == "stead":
            df = df.replace('',np.nan).groupby('receiver_code', as_index=False).first().fillna('')
            df[columns_].to_csv(path+Path(arrival_fname).stem+".csv",mode='a', header=False, index=False)
            # pruge df
            df = df[0:0]
        #save data pha
        else:
            df = df[~df['year'].isna()]
            df.reset_index(inplace = True, drop = True)
            df2dat(df,evnum = 0, path = path, fname=Path(arrival_fname).stem+'.dat', mode = 'a', verbose=False)
            # pruge df
            df = df[0:0]    
        print(f"processing {eventid_}")
        event_counter += 1
        trigger_counter = 0

print("convert finish!")