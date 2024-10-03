import os
from openai import OpenAI
import json

OPENAI_API_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 50 seconds (approximately 140 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.
        Whatever you create should be relevant to the question, not outside of it. When you are asked questions about Hemp plant never discuss it's 
        health benefits. Only industrial.

        For instance, if the user asks a question:
        
        You would produce content like this:
        What is Industrial Hemp?
        Here is the information on the question
        -It is specifically grown for industrial purposes such as textiles, paper, and biodegradable plastics.
        -Contains low levels of THC (tetrahydrocannabinol), typically less than 0.3%, making it non-psychoactive.
        -Rich in CBD (cannabidiol), which is used in various medical and wellness products.
        -Hemp fibers are known for being strong and durable, often used in rope, clothing, and construction materials.
        -The seeds are used for nutritional products like hemp oil, protein powder, and food supplements.
        -Hemp is a renewable resource that grows quickly and requires fewer pesticides or herbicides.
        -It is considered environmentally friendly due to its ability to absorb carbon dioxide and improve soil health.
        -Hemp can be processed into biofuels, insulation materials, and even as a replacement for certain plastics.

        You are now tasked with creating the best short script based on the user's requested type of question.

        Keep it brief, highly interesting, and unique.

        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )

    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
