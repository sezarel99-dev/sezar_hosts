import os, sys, subprocess, traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8305870987:AAGAEsj_Mqib0ZkDMBFXjX6sbHv6L-dR4sM")
MY_ID = int(os.getenv("8013770402", "8013770402"))
os.makedirs("tools", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    await update.message.reply_text("✅ بوت الاستضافة شغال على Render\nارسل أي ملف .py")

def run_tool(path):
    try:
        p = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=60, cwd="tools")
        out = (p.stdout or "") + "\n" + (p.stderr or "")
        return out if out.strip() else "✅ اشتغل بدون مخرجات"
    except subprocess.TimeoutExpired:
        return "❌ طول أكثر من 60 ثانية وتم ايقافه"
    except Exception:
        return traceback.format_exc()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID:
        await update.message.reply_text("❌ مو مسموح")
        return
    doc = update.message.document
    if not doc.file_name.endswith(".py"):
        await update.message.reply_text("❌ فقط .py")
        return
    f = await context.bot.get_file(doc.file_id)
    path = f"tools/{doc.file_name}"
    await f.download_to_drive(path)
    await update.message.reply_text(f"📥 تم حفظ {doc.file_name}\n⏳ جاري التشغيل...")
    res = run_tool(path)
    await update.message.reply_text(f"📤 نتيجة {doc.file_name}:\n\n{res[:3800]}")

async def list_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    files = os.listdir("tools")
    await update.message.reply_text("📁 الأدوات:\n" + "\n".join(files) if files else "لا يوجد أدوات")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_tools))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("Bot Started")
    app.run_polling()
