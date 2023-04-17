'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''

import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = "e2483d798f4145498e2817172c5ee9c4"
service_region = "eastus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "en-GB-OliverNeural"

# text = "Louis Le Nain lived in a region to the north of Paris known for its open fields that produced cereals and grain. Although he settled in Paris with his two brothers, who were also painters, he produced a series of rural images that recall the landscape of his youth. In the Landscape with Peasants, an old woman regards three children: a little girl dressed in white collar and cap, a small boy who plays the pipe, and a boy dressed in a cloak and hat who plays a hurdy-gurdy."

text = "\"Two Girls under an Umbrella,\" a 1910 painting by the German Expressionist artist Ernst Ludwig Kirchner, captures a moment of companionship between two women sharing an umbrella in a rural setting. This work is emblematic of Kirchner's style, characterized by bold colors, energetic brushstrokes, and a focus on capturing the emotional essence of a scene."

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

result = speech_synthesizer.speak_text_async(text).get()
# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

