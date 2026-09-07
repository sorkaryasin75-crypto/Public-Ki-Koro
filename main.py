import asyncio
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError

# --- কনফিগারেশন ---
BOT_TOKEN = "8724006661:AAFNXK3qskksYUNJ_fVJQRia72_aNtGjMwY"  # আপনার বট টোকেন দিন
CHAT_ID = "-1002352180501"  # আপনার টেলিগ্রাম গ্রুপের CHAT ID দিন (অবশ্যই মাইনাস সহ)

bot = Bot(token=BOT_TOKEN)

# --- Crypto & Blockchain Tips Collection ---
CRYPTO_TIPS = [
    # 🪙 Fundamentals & Security
    "🪙 Crypto Tip: কখনো কোনো অপরিচিত লিংকে আপনার Wallet Connect করবেন না এবং Seed Phrase শেয়ার করবেন না।",
    "🛡️ Crypto Security: ফান্ড নিরাপদ রাখতে সবসময় Hardware Wallet (যেমন Ledger/Trezor) বা Trust Wallet ব্যবহার করুন।",
    "🪙 Crypto Tip: 'Not your keys, not your coins'—সেন্ট্রালাইজড এক্সচেঞ্জে ফান্ড রাখা শতভাগ নিরাপদ নয়।",
    "🛡️ Crypto Security: সেন্ট্রালাইজড এক্সচেঞ্জ (Binance, Bybit) ব্যবহারে অবশ্যই 2FA (Google Authenticator) অন রাখুন।",
    "🪙 Crypto Tip: সাইন-ইন করার আগে সবসময় ওয়েবসাইটের URL ভালোভাবে দেখে নিন, Phishing সাইট থেকে সাবধান থাকুন।",

    # 📊 Trading & Risk Management
    "📊 Crypto Trading: ক্রিপ্টোতে ইনভেস্ট করার মূল নিয়ম—ততটুকুই ইনভেস্ট করুন যা হারানোর মানসিকতা আপনার আছে।",
    "📈 Risk Management: ট্রেড নেওয়ার আগে অবশ্যই Stop-Loss ব্যবহার করুন, এটি আপনার বড় ক্ষতি থেকে রক্ষা করবে।",
    "📊 Crypto Trading: FOMO (Fear Of Missing Out) এর চক্করে পড়ে কোনো কয়েন অল-টাইম হাই (ATH)-এ বাই করবেন না।",
    "📈 Risk Management: আপনার সম্পূর্ণ পোর্টফোলিও কখনো একটি কয়েনে রাখবেন না, পোর্টফোলিও Diversify করুন।",
    "📊 Crypto Trading: ট্রেডিংয়ের সময় নিজের আবেগ (Fear & Greed) নিয়ন্ত্রণ রাখা সফলতার অন্যতম বড় শর্ত।",

    # 💡 Investment Strategies (DCA & Web3)
    "💡 Investment Strategy: মার্কেট ভোলাটিলিটি এড়াতে DCA (Dollar-Cost Averaging) মেথড ব্যবহার করে কয়েন বাই করুন।",
    "🌐 Web3 Tip: কোনো নতুন কয়েনে ইনভেস্ট করার আগে সেটির Whitepaper এবং Tokenomics ভালোভাবে এনালাইসিস করুন।",
    "💡 Investment Strategy: বিটকয়েন হালভিং (Halving) সাইকেল পর্যবেক্ষণ করে দীর্ঘমেয়াদী ইনভেস্টমেন্ট প্ল্যান করুন।",
    "🌐 Web3 Tip: Airdrop হান্টিংয়ের জন্য টেস্টনেট এবং মেইননেট ইন্টারঅ্যাকশনের সময় সবসময় সেপারেট ওয়ালেট ব্যবহার করুন।",
    "💡 Investment Strategy: ফান্ডামেন্টালি শক্তিশালী কয়েন (BTC, ETH) পোর্টফোলিওতে বেশি রাখার চেষ্টা করুন।",

    # 🚀 Market Basics & Terminology
    "🚀 Crypto Term: Bull Market মানে মার্কেট ঊর্ধ্বমুখী এবং Bear Market মানে দাম নিম্নমুখী থাকা।",
    "🔍 Analysis Tip: অন-চেইন এনালাইসিসের জন্য Glassnode এবং CryptoQuant এর মতো প্ল্যাটফর্ম ব্যবহার করতে পারেন।",
    "🚀 Crypto Term: Market Cap = Total Coin Supply × Current Price। শুধু কয়েনের দাম দেখে প্রজেক্ট বিচার করবেন না।",
    "🔍 Analysis Tip: CoinMarketCap বা CoinGecko ব্যবহার করে কয়েনের মোট সাপ্লাই এবং সার্কুলেটিং সাপ্লাই চেক করুন।",
    "🚀 Crypto Term: TVL (Total Value Locked) নির্দেশ করে একটি DeFi প্রজেক্টে কত পরিমাণ ফান্ড জমা আছে।"
]

# ১০০০+ অটো-মেসেজ চক্র সচল রাখার জন্য ডাইনামিক ফিলিং
for i in range(len(CRYPTO_TIPS) + 1, 501):
    category = random.choice(["🪙 Crypto Tip", "📊 Trading Strategy", "🛡️ Security Alert", "🌐 Web3 Advice"])
    CRYPTO_TIPS.append(f"{category} #{i}: কন্টিনিউয়াস লার্নিং ও ধৈর্যই ক্রিপ্টো মার্কেট থেকে ভালো প্রফিট বের করার মূল চাবিকাঠি।")


# অটোমেটিক মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_messages():
    while True:
        try:
            # র‍্যান্ডম ক্রিপ্টো মেসেজ সিলেক্ট
            message_text = random.choice(CRYPTO_TIPS)
            
            await bot.send_message(chat_id=CHAT_ID, text=message_text)
            print("[SUCCESS] ক্রিপ্টো মেসেজ গ্রুপে সফলভাবে পাঠানো হয়েছে।")
            
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

app = FastAPI(title="Crypto Tips Auto Notifier", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "message": "Crypto Auto Notifier System Active"}
