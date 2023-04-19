# goodmorning
Make gpt-3.5 wish you a good day and give you a weather-forecast using open data from SMHI.

## Requirements
The `requests` module for python.

## Usage
Create the files `apikey.txt` and `longlat.txt`. In `apikey.txt` you should put your openai api-key. 
In the `longlat.txt`-file you should put on two separate rows the longitude and latitude of the point where you want to fetch
the weather-info from. **Note**: the location should probably be in- or around Sweden, as the weather info is fetched from SMHI.

Then just run the `goodmorning.py` program.

Example (Line-wrapped):
```
$ python3 goodmorning.py 
Good morning! It's April 20th and it looks like we're in for a beautiful day. 
The sky is clear this morning and the sun is shining bright. 
As we move along into the afternoon, conditions will remain the same, with 
clear skies throughout the day. You won't need to worry about bringing an 
umbrella or wearing a jacket because the weather will be quite mild. 
In the evening, the clear sky will provide a beautiful sunset. 
Enjoy this lovely day and make the most of it!
```
