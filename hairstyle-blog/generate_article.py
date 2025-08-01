import os
import datetime
import google.generativeai as genai

# --- Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
# Use a model that supports image generation. For example, 'gemini-pro-vision'
# NOTE: As of my last update, text-to-image generation is not directly available in the public Gemini API.
# This script assumes such functionality exists. The user might need to use a different model or a different API for image generation.
# For this example, I will use a placeholder function for image generation.
image_model = genai.GenerativeModel(model_name="gemini-pro-vision", # Placeholder model
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
text_model = genai.GenerativeModel(model_name="gemini-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

# --- Date and Paths ---
now = datetime.datetime.now()
year = now.year
month = now.month
month_str = f"{month:02d}"

article_dir = os.path.join(os.path.dirname(__file__), "articles")
image_dir = os.path.join(article_dir, "images", f"{year}-{month_str}")
os.makedirs(image_dir, exist_ok=True)

article_path = os.path.join(article_dir, f"{year}-{month_str}.html")
index_path = os.path.join(os.path.dirname(__file__), "index.html")

# --- Content Generation ---
def generate_image(prompt, path):
    """Placeholder for image generation.
    In a real scenario, this would call the Gemini API to generate an image and save it.
    """
    print(f"Generating image for prompt: '{prompt}' and saving to {path}")
    # Placeholder: Create a dummy image file
    with open(path, "w") as f:
        f.write(f"<html><body><p>Image for: {prompt}</p></body></html>")
    return path

def generate_html_content(year, month):
    """Generates the HTML content for the article."""
    # Prompts for the text model
    main_prompt = f"'{year}년 {month}월 최신 헤어스타일 트렌드'에 대한 블로그 게시물을 작성해줘."
    # Prompts for the image model
    trend_prompts = [f"A model with a stylish {hairstyle} haircut." for hairstyle in ["bob", "pixie", "long layers", "shag", "curtain bangs", "mullet", "buzz cut", "french bob", "wolf cut", "jellyfish cut"]]
    celebrity_prompts = [f"A celebrity with a trendy {hairstyle} hairstyle." for hairstyle in ["bob", "pixie", "long layers", "shag", "curtain bangs", "mullet", "buzz cut", "french bob", "wolf cut", "jellyfish cut"]]

    # Generate main text content
    # response = text_model.generate_content(main_prompt)
    # main_content = response.text
    main_content = "This is a placeholder for the main content of the article. The Gemini API would generate this."


    # Generate images
    trend_image_paths = []
    for i, prompt in enumerate(trend_prompts):
        image_path = os.path.join(image_dir, f"trend_{i}.png")
        generate_image(prompt, image_path)
        trend_image_paths.append(os.path.relpath(image_path, article_dir))

    celebrity_image_paths = []
    for i, prompt in enumerate(celebrity_prompts):
        image_path = os.path.join(image_dir, f"celebrity_{i}.png")
        generate_image(prompt, image_path)
        celebrity_image_paths.append(os.path.relpath(image_path, article_dir))


    # Create HTML structure
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{year}년 {month}월 최신트랜드</title>
</head>
<body>
    <h1>{year}년 {month}월 최신트랜드</h1>
    <p>{main_content}</p>
    <h2>최신 헤어스타일 트렌드</h2>
    {''.join([f'<img src="{path}" alt="Trend Hairstyle {i+1}"><br>' for i, path in enumerate(trend_image_paths)])}
    <h2>연예계 최신 헤어스타일</h2>
    {''.join([f'<img src="{path}" alt="Celebrity Hairstyle {i+1}"><br>' for i, path in enumerate(celebrity_image_paths)])}
</body>
</html>
"""
    return html

# --- File Operations ---
def update_index_file(year, month):
    """Updates the index.html file with a link to the new article."""
    new_link = f'<li><a href="articles/{year}-{month:02d}.html">{year}년 {month}월</a></li>'
    with open(index_path, "r+") as f:
        content = f.read()
        # Add the new link before the placeholder comment
        content = content.replace("<!-- Links to monthly articles will be added here -->", f"{new_link}\n        <!-- Links to monthly articles will be added here -->")
        f.seek(0)
        f.write(content)

# --- Main Execution ---
if __name__ == "__main__":
    print("Generating monthly hairstyle trend article...")
    html_content = generate_html_content(year, month)
    with open(article_path, "w") as f:
        f.write(html_content)
    print(f"Article created at {article_path}")

    update_index_file(year, month)
    print(f"Index file updated at {index_path}")
    print("Done.")
