import os
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"  

    audiobj = gTTS(
        text=input_text,
        lang=language,  
        slow=False
    )
    
    
    audiobj.save(output_filepath)
    print(f"✅ Speech saved to: {output_filepath}")


input_text = " There are plenty of solutions to acne" 

text_to_speech_with_gtts(input_text, output_filepath="gtts_testing.mp3")
