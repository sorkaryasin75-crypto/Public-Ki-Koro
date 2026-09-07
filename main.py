import asyncio
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError

# --- কনফিগারেশন ---
BOT_TOKEN = "8724006661:AAF0xcleV67AbrFfLhJ2LvUMoh9m_UFG7dA"  # আপনার বট টোকেন দিন
CHAT_ID = "-1002352180501"  # আপনার টেলিগ্রাম গ্রুপের CHAT ID দিন (অবশ্যই মাইনাস সহ)

bot = Bot(token=BOT_TOKEN)

# --- NIVA, NS, Top Coin, Coinsta & New Coins Collection ---
COIN_TIPS = [
    # 🪙 NIVA COIN
    "🪙 Niva Coin Update: Niva Coin মাইনিংয়ে আপনার Secret Key বা পাসওয়ার্ড কখনোই কারো সাথে শেয়ার করবেন না।",
    "⚡ Niva Coin Tip: Niva-Miners প্যানেল ব্যবহার করার সময় অফিসিয়াল টেলিগ্রাম চ্যানেল থেকে সঠিক আপডেট যাচাই করে নিন।",
    "🪙 Niva Coin Info: Niva Mining সিস্টেম থেকে উইথড্র বা রিওয়ার্ড দাবি করার আগে মিনিমাম ব্যালেন্স শর্ত দেখে নিন।",

    # 🚀 NS COIN & NEW TOP COINS
    "🚀 NS Coin Update: নতুন এয়ারড্রপ ও Tap-To-Earn কয়েনের ক্ষেত্রে বট ভেরিফাইড কি না তা আগে নিশ্চিত করুন।",
    "🔥 New Top Coin: সাম্প্রতিক ট্রেন্ডিং Telegram Bot Mining টোকেনগুলোতে সময়মতো ডেলি টাস্ক ও ক্লেম সম্পন্ন করুন।",
    "💎 Top Coin Strategy: নতুন টপ কয়েনগুলোতে রেফারেল বোনাস বাড়াতে মেম্বারদের সঠিক গাইড প্রদান করুন।",
    "🚀 NS Coin Tip: নতুন কয়েন লিস্ট হওয়ার আগে ডিসেন্ট্রালাইজড ওয়ালেট (যেমন Tonkeeper বা Phantom) রেডি রাখুন।",

    # 📊 COINSTA & MARKET ANALYTICS
    "📊 Coinsta Market Tip: CoinStats / Coinsta থেকে কয়েনের রিয়েল-টাইম প্রাইস ও ভলিউম ট্রাক করে সিদ্ধান্ত নিন।",
    "📈 Crypto Market: যেকোনো New Top Coin-এ যুক্ত হওয়ার আগে প্রজেক্টের Tokenomics ও রোডম্যাপ ভালোভাবে দেখে নিন।",
    "📊 Coinsta Trend: কোনো নতুন কয়েন মার্কেটে আসতেই হুট করে ফ্যান্ড ইনভেস্ট না করে কমিউনিটি ফিডব্যাক পর্যবেক্ষণ করুন।",

    # 🛡️ AIRDROP & BOT SAFETY
    "🛡️ Safety Alert: Telegram Mining Bot-এ কাজ করার সময় কখনোই মূল প্রাইমারি ক্রিপ্টো ওয়ালেট কানেক্ট করবেন না, সেকেন্ডারি ওয়ালেট ব্যবহার করুন।",
    "💡 Mining Tip: প্রতিদিনের ডেলি ডেইলি কম্বো, কুইজ এবং টাস্ক পুরন করলে ফ্রিতে অতিরিক্ত পয়েন্ট পাওয়া যায়।",
    "🛡️ Security Reminder: কোনো Bot যদি কয়েন ক্লেইম করার জন্য আগে থেকে টাকা/গ্যাস ফি দাবি করে, তবে স্ক্যাম হওয়ার সম্ভাবনা থাকে।",
    "💡 Top Coin Guide: Telegram Web3 ইকোসিস্টেমের মেমে ও ইউটিলিটি কয়েনগুলো সম্পর্কে আপডেট থাকতে অন-চেইন ডাটা ফলো করুন।"
]

# ১০০০+ অটো-মেসেজ চক্র সচল রাখার জন্য ডাইনামিক ফিলিং
for i in range(len(COIN_TIPS) + 1, 501):
    category = random.choice(["🪙 Niva & NS Coin Update", "🔥 New Top Coin Alert", "📊 Coinsta Market Tip", "🛡️ Bot Security"])
    COIN_TIPS.append(f"{category} #{i}: নতুন টেলিগ্রাম কয়েন ও মাইনিং প্রজেক্টের যেকোনো বড় আপডেট পেতে গ্রুপের সাথেই থাকুন।")


# অটোমেটিক মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_messages():
    while True:
        try:
            # র‍্যান্ডম কয়েন সংক্রান্ত মেসেজ সিলেক্ট
            message_text = random.choice(COIN_TIPS)
            
            await bot.send_message(chat_id=CHAT_ID, text=message_text)
            print("[SUCCESS] কয়েন সম্পর্কিত মেসেজ গ্রুপে সফলভাবে পাঠানো হয়েছে।")
            
        except TelegramError as e:
            print(f"[ERROR] মেসেজ পাঠাতে সমস্যা হয়েছে: {e}")
        except Exception as e:
            print(f"[ERROR] অজানা সমস্যা: {e}")
            
        # ৬ মিনিট পর পর মেসেজ পাঠাবে (৬ মিনিট = ৩৬০ সেকেন্ড)
        await asyncio.sleep(360)

# Lifespan ইভেন্ট (FastAPI সার্ভার চালু ও বন্ধ হওয়ার সময় রান করবে)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # সার্ভার চালু হওয়ার সাথে সাথে ব্যাকগ্রাউন্ড টাস্ক শুরু হবে
    task = asyncio.create_task(auto_send_messages())
    yield
    # সার্ভার বন্ধ হলে টাস্ক ক্যানসেল হবে
    task.cancel()

app = FastAPI(title="Crypto Coin Auto Notifier", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "message": "Coin Auto Notifier System Active"}
