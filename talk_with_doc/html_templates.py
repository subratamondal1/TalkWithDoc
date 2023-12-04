from PIL import Image
import base64

bot_image = Image.open("../images/ai.png")
# Encode the image in base64
with open("../images/ai.png", "rb") as image_file:
    bot_image_base64 = base64.b64encode(image_file.read()).decode()

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2f4f4f
}
.chat-message.bot {
    background-color: #004242
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  object-fit: cover;
  clip-path: circle(50%);
}

.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.svgrepo.com/show/416649/cog-gear-settings.svg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.svgrepo.com/show/416659/user-profile-person.svg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''