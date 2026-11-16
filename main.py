from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from database import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    create_tables
)

BOT_TOKEN = "B0T TOKEN"


def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ افزودن کار", callback_data="add")],
        [InlineKeyboardButton("📋 نمایش کارها", callback_data="tasks")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "به بات مدیریت کارهای روزانه خوش اومدی.\n\n"
        "https://github.com/0MORADI0",
        reply_markup=main_keyboard()
    )


async def show_tasks(update, context):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)
    keyboard = []

    if not tasks:
        text = "📋 هنوز کاری ثبت نکردی!"
        keyboard.append([
            InlineKeyboardButton("➕ افزودن کار", callback_data="add")
        ])

    else:
        text = "📋 لیست کارهای شما:\n\n"

        for task_id, title, is_done in tasks:
            status = "✅" if is_done else "❌"
            text += f"{status} {task_id}. {title}\n"

            buttons = []

            if not is_done:
                buttons.append(
                    InlineKeyboardButton(
                        "✅ تکمیل",
                        callback_data=f"done_{task_id}"
                    )
                )

            buttons.append(
                InlineKeyboardButton(
                    "🗑 حذف",
                    callback_data=f"delete_{task_id}"
                )
            )

            keyboard.append(buttons)

        keyboard.append([
            InlineKeyboardButton("➕ افزودن کار", callback_data="add")
        ])

    keyboard.append([
        InlineKeyboardButton("🔙 منوی اصلی", callback_data="menu")
    ])

    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=markup
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=markup
        )


async def button_handler(update, context):
    query = update.callback_query
    data = query.data

    if data == "add":
        await query.answer()
        context.user_data["waiting_add"] = True

        await query.message.reply_text(
            "عنوان کاری که می‌خوای ثبت کنی رو بفرست:"
        )

    elif data == "tasks":
        await query.answer()
        await show_tasks(update, context)

    elif data == "menu":
        await query.answer()
        await query.edit_message_text(
            "منوی اصلی:\n\nچه کاری می‌خوای انجام بدی؟",
            reply_markup=main_keyboard()
        )

    elif data.startswith("done_"):
        task_id = int(data.split("_")[1])

        success = complete_task(
            update.effective_user.id,
            task_id
        )

        if success:
            await query.answer("کار با موفقیت تکمیل شد! 🎉")
        else:
            await query.answer("کار پیدا نشد!")

        await show_tasks(update, context)

    elif data.startswith("delete_"):
        task_id = int(data.split("_")[1])

        success = delete_task(
            update.effective_user.id,
            task_id
        )

        if success:
            await query.answer("کار با موفقیت حذف شد! 🗑")
        else:
            await query.answer("کار پیدا نشد!")

        await show_tasks(update, context)


async def text_handler(update, context):
    if context.user_data.get("waiting_add"):
        title = update.message.text.strip()

        if not title:
            await update.message.reply_text(
                "عنوان کار نمی‌تونه خالی باشه."
            )
            return

        task_id = add_task(
            update.effective_user.id,
            title
        )

        context.user_data["waiting_add"] = False

        await update.message.reply_text(
            f"کار با موفقیت ثبت شد! ✅\n\n"
            f"شناسه: {task_id}\n"
            f"عنوان: {title}",
            reply_markup=main_keyboard()
        )


async def help_command(update, context):
    await update.message.reply_text(
        "از دکمه‌های زیر برای مدیریت کارهات استفاده کن:",
        reply_markup=main_keyboard()
    )


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()