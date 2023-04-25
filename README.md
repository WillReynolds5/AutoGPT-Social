<!DOCTYPE html>
<html>
<body>
	<h1>🤖 AutoGPT-Social 📸</h1>
	<p>🚀 This Instagram bot app automatically generates and posts engaging content for your Instagram account using OpenAI GPT. The bot gets real-world feedback in the form of likes and comments and uses the data to optimize captions, hashtags, and posting times. The bot's goal is to get as many likes, comments, and followers as possible. 💯</p>
<h2>🌟 Features</h2>
<ul>
	<li>🖼️ Automatically selects images and generates captions w/ hashtags for Instagram posts</li>
    <li>📈 Gets real-time feedback (number of likes, comments) to optimize posting schedule, captions, and hashtags for maximum views, likes, comments, and follows</li>
	<li>⏲️ Set the number of posts per day</li>
	<li>🔍 Automatically finds 100s of relevant hashtags and figures out which are best</li>
</ul>
<h2>🛠️ Setup and Installation</h2>
<ol>
	<li>🐍 Make sure you have Python 3.x installed (tested on 3.8). You can download it from <a href="https://www.python.org/downloads/">here</a>.</li>
	<li>💻 <code>pip install openai instagrapi Pillow</code></li>
	<li>📦 Clone this repository:<br>
	<code>git clone https://github.com/WillReynolds5/AutoGPT-Social.git</code><br>
	<code>cd AutoGPT-Social</code></li>
</ol>
<h2>📚 Usage</h2>
<ol>
	<li>🔑 Add an Instagram account and OpenAI API key:<br>
	<code>python initialize_bot.py &lt;instagram_username&gt; &lt;instagram_password&gt; &lt;openai_api_key&gt;</code></li>
	<p>🗂️ This script will create a directory for the specified Instagram account, set up the required directory structure, and save the account configuration in a JSON file.</p>
	<li>📝 Input will ask that you enter an account summary: <code>&lt;your_account_summary&gt;</code> <br> ie. The posts should be centered around adding value to viewers' lives by creating informative copy about tips, trends, and fun ideas in the areas of gardening, interior design, architecture, and real estate in general.</li>
	<li>🏷️ Input will ask that you enter at least one relevant hashtag (separate multiple by commas)<code>&lt;your_hashtags&gt;</code> <br> ie. #realestate, #design</li>
	<li>✏️ (Optional) Edit <code>accounts/&lt;instagram_username&gt;/prompt.txt</code> if you want to customize the mission statement or objectives for the bot.</li>
	<li>➕ Add all of your images to the <code>accounts/&lt;instagram_username&gt;/queue</code> directory. The bot will select images from this directory to post on Instagram.</li>
    <li>📷 Give your images simple yet descriptive titles so the bot knows what is in them (separate words with _) ie. photo_of_golden_gate_bridge.jpg</li>
    <li>🚀 Run the Instagram bot with the specified account directory and desired number of posts per day:<br>
	<code>python start_bot.py &lt;instagram_username&gt; &lt;post_count&gt;</code></li>
	<p>🔄 Replace &lt;instagram_username&gt; with the appropriate Instagram username directory created by the <code>initialize_bot.py</code> script and &lt;post_count&gt; with the desired number of posts per day.</p>
</ol>
<!-- Add this section where you want to include the table -->
<section>
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
                <th colspan="2">Sample</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <img src="sample/modern_design.jpg" alt="Image" width="200"><br>
                    <span>modern_design.jpg</span>
                </td>
                <td>
                    <p>Sample Post:</p>
                    <p>Looking for ways to bring a modern touch to your home? Here are a few tips:<br><ul>
                    <li>Incorporate clean lines and geometric shapes in your furniture and decor</li>
                    <li>Use a neutral color palette with pops of bold colors for contrast</li>
                    <li>Add light fixtures with a modern design to enhance the space</li>
                    </ul>
        <p>Follow us for more informative posts about architecture, interior design, gardening, and real estate. Don't forget to use these related hashtags in your posts to join the conversation: #griffith_partners #moderndesign #homedecor #interiordesign #architecture.</p>
                </td>
            </tr>
        </tbody>
    </table>
</section>
<h2>Coming Soon!</h2>
<ul>
	<li>Support for twitter. Want other platforms? DM me on twitter @spacemonkeyai</li>
	<li>AI Image generation</li>
</ul>

<h2>Notes</h2>
<ul>
	<li>The Instagram bot app uses GPT-3.5-turbo and OpenAI's API to generate captions. Make sure you have a valid OpenAI API key.</li>
	<li>The app is not responsible for any consequences of using the bot, such as Instagram account restrictions or bans. Use it at your own risk.</li>
</ul>
</body>
</html>
