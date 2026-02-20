#!/usr/bin/env python3
"""WhatsApp quick sender without token.

This tool only asks for the recipient number, then opens WhatsApp chat links.
Actual sending remains user-confirmed inside WhatsApp.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.parse
import webbrowser

PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")
DEFAULT_MESSAGE = "السلام علييكم"
DEFAULT_COUNT = 3


def normalize_phone(raw_phone: str) -> str:
    cleaned = raw_phone.strip().replace(" ", "").replace("-", "")
    if not PHONE_RE.match(cleaned):
        raise ValueError("رقم غير صالح. مثال صحيح: +201001234567")
    return cleaned.lstrip("+")


def build_wa_url(phone: str, message: str) -> str:
    if not message.strip():
        return f"https://wa.me/{phone}"
    query = urllib.parse.urlencode({"text": message})
    return f"https://wa.me/{phone}?{query}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="فتح واتساب بإدخال رقم المستلم فقط (بدون توكن)",
    )
    parser.add_argument("--to", help="رقم المستلم بصيغة دولية (مثال: +9647xxxxxxxx)")
    parser.add_argument(
        "--message",
        "-m",
        default=DEFAULT_MESSAGE,
        help=f"نص الرسالة الافتراضي: {DEFAULT_MESSAGE}",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=f"عدد مرات فتح الرابط (الافتراضي: {DEFAULT_COUNT})",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0.5,
        help="فاصل زمني بين الفتحات بالثواني",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    to_input = args.to or input("أدخل رقم المستلم بصيغة دولية: ").strip()

    try:
        to_phone = normalize_phone(to_input)
    except ValueError as err:
        print(f"خطأ: {err}")
        return 1

    if args.count < 1:
        print("خطأ: --count يجب أن يكون 1 أو أكثر")
        return 1

    if args.delay_seconds < 0:
        print("خطأ: --delay-seconds يجب أن يكون 0 أو أكثر")
        return 1

    url = build_wa_url(to_phone, args.message)
    print(f"تم إنشاء رابط واتساب: {url}")

    for i in range(1, args.count + 1):
        opened = webbrowser.open(url)
        if opened:
            print(f"تم فتح الرابط {i}/{args.count}")
        else:
            print(f"تعذر فتح المتصفح تلقائيًا في المحاولة {i}. افتح الرابط يدويًا:")
            print(url)
            return 1

        if i < args.count and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)

    print("اكتمل. أرسل الرسالة من داخل واتساب.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
