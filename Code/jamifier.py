import pandas as pd
import jams
import librosa
import os
from typing import Tuple
import yaml
from yaml.loader import SafeLoader

#TODO: We have to change the curator and anotator data to the dataset's one

# Let's check how our data works
# We are focusing on the data of an individual song in order to understand:
def generateJams():
    files = os.listdir("./Melody1/")
    for f in files:
        
        df = pd.read_csv(f"./Melody1/{f}")
       
        df.columns = ["Time", "Hz"]

        time_values = df["Time"].values
        hz_values = df["Hz"].values

        jam = jams.JAMS()
        jam.file_metadata.duration = time_values[len(time_values) -1]
        title =""
        with open(f'./Metadata/{f[:-11]}METADATA.yaml') as fi:
            data = yaml.load(fi, Loader=SafeLoader)
            jam.file_metadata.title =data["title"]
            title = data["title"]
        note = jams.Annotation(namespace="note_hz")
        note.annotation_metadata=jams.AnnotationMetadata(curator={"name": "Rachel Bittner", "email": None },
                                                        version="1.0.0",
                                                        data_source='MEDLEYDB',
                                                        annotator= {"name": "Mike Tierney"})
        for index in range(0, len(time_values)):
            note.append(time=time_values[index], duration= 0, value= hz_values[index])
        jam.annotations.append(note)
        jam.save(f"./jams/{title}.jams")

generateJams()
        

