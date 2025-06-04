QuickBite - Your Campus Foodie Friend! 🍔🍟🍕
QuickBite is a super cool web app built with Flask that makes ordering food on campus a breeze for students! No more long queues or missed meals – just quick, delicious bites delivered right to you. 🚀

✨ Awesome Features You'll Love! ✨
Student Central! 🎓 Register for an account and log in securely to unlock all the yummy features.
Feast Your Eyes! 🤩 Browse a mouth-watering menu with tempting descriptions, prices, and even emojis for every dish!
Your Personal Food Basket! 🛒 Add all your favorites to your shopping cart and adjust quantities with ease.
Order Up! 🛎️ Checkout seamlessly to place your order. It's as easy as pie!
My Food Journey! 📜 Keep track of all your past and current orders in one place.
Live Order Updates! ⏰ Get real-time status updates on your order so you know exactly when to expect your grub.
Oops! Need to Cancel? ↩️ Life happens! You can cancel orders (with a friendly limit of 2 cancellations to keep things fair).
Your QuickBite Profile! 👤 See your personal details and cool stats about your ordering habits.

🛠️ Tech Goodies Under the Hood 🛠️
Flask: Our speedy Python web framework. 🐍
MySQL: Where all your delicious order data lives! 💾
HTML/CSS: Making QuickBite look good and feel intuitive. ✨
JavaScript: Adding that extra sprinkle of interactivity (like adding to cart!). 🖱️
Werkzeug Security: Keeping your passwords safe and sound. 🔒
mysql-connector-python: The bridge between our app and the database. 🌉
🚀 Get QuickBite Running! 🚀
1. Grab the Code! 💻
Bash

git clone https://github.com/your-username/QuickBite.git
cd QuickBite
2. Create Your Own Space (Virtual Environment)! 🌳
It's a good practice to keep your project's dependencies neatly organized.

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install the Essentials! 📦
Bash

pip install Flask mysql-connector-python Werkzeug
4. Database Magic! ✨
Create Your Database: Make sure your MySQL server is running, then create a database named quickbite_db.

SQL

CREATE DATABASE quickbite_db;
Tell QuickBite Your MySQL Secrets:
Open app.py and update the MYSQL_CONFIG with your MySQL username and password:

Python

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_Password', 
    'database': 'quickbite_db',
    'autocommit': True
}
Tables, Assemble!:
The create_tables() function automatically sets up all the necessary tables and even adds some sample menu items for you when the app starts. 🎉

5. Fire It Up! 🔥
Bash

python app.py
You'll usually find QuickBite ready to go at http://127.0.0.1:5000/.

📂 Peek Inside QuickBite! 📂
QuickBite/
├── app.py                     # The heart of our Flask app! ❤️
├── static/
│   ├── css/
│   │   └── style.css          # Making everything pretty! 💅
│   └── js/
│       └── main.js            # Adding some sparkle! ✨
└── templates/
    ├── base.html              # The foundation for all our pages. 🏗️
    ├── home.html              # Welcome to QuickBite! 👋
    ├── login.html             # Your gateway to deliciousness. 🚪
    ├── menu.html              # All the yummy food options! 😋
    ├── orders.html            # Your food journey, past and present. 🗺️
    ├── order_status.html      # Track your munchies in real-time! ⏱️
    ├── payment_success.html   # Hooray, your order is placed! 🎉
    ├── profile.html           # Your QuickBite identity. 🌟
    └── cancel_order.html      # For those change-of-mind moments. 🤔
📝 How to Use QuickBite 📝
New Student? 🧑‍🎓 Register with your name, student ID, email, and a secret password.
Already Here? 🙋‍♀️ Log in with your email and password.
Explore the Menu! 📖 Discover all the tasty treats available.
Fill Your Cart! 🛍️ Click to add items and adjust quantities to your heart's content.
Time to Checkout! 💳 Confirm your order and get ready to eat!
My Orders, My History! 📊 See all your fantastic food choices.
Order Tracker! 📍 Click on an order to see its live status – is it being cooked? On its way?
Need to Undo? 🙅‍♀️ You can cancel orders that are 'Placed' or 'In Progress' (remember the 2-cancellation limit!).
Your QuickBite Story! 📊 Your profile shows off your order stats and details.
See Ya Later! 👋 Log out when you're done for the day.
🙌 Want to Contribute? 🙌
We'd love your help to make QuickBite even better! Here's how you can join the fun:

Fork this repository. 🍴
Create a new branch (git checkout -b feature/your-awesome-feature). 🌿
Make your brilliant changes. 🌟
Commit your work (git commit -m 'Added an amazing new feature!'). 📝
Push your changes to your branch (git push origin feature/your-awesome-feature). ⬆️
Open a Pull Request! 🎉
📜 License 📜
This project is open source and available under the MIT License. Share the love! ❤️


This is Quick Bites!!!
