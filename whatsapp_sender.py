#!/usr/bin/env python3
"""Send WhatsApp text messages via official WhatsApp Cloud API."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")
GRAPH_API_VERSION = "v23.0"
DEFAULT_TO = "+9647734549509"
DEFAULT_MESSAGE = "السلام علييكم"
DEFAULT_COUNT = 3


def normalize_phone(raw_phone: str) -> str:
    cleaned = raw_phone.strip().replace(" ", "").replace("-", "")
    if not PHONE_RE.match(cleaned):
        raise ValueError("رقم غير صالح. مثال صحيح: +201001234567")
    return cleaned.lstrip("+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="إرسال رسائل واتساب تلقائيًا عبر WhatsApp Cloud API الرسمي",
    )
    parser.add_argument(
        "--to",
        default=DEFAULT_TO,
        help=f"رقم المستلم (الافتراضي: {DEFAULT_TO})",
    )
    parser.add_argument(
        "--message",
        "-m",
        default=DEFAULT_MESSAGE,
        help=f"نص الرسالة (الافتراضي: {DEFAULT_MESSAGE})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=f"عدد الرسائل المتتالية (الافتراضي: {DEFAULT_COUNT})",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0.0,
        help="فاصل زمني بين الرسائل بالثواني (اختياري)",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("WHATSAPP_TOKEN", ""),
        help="Access token (أو من المتغير WHATSAPP_TOKEN)",
    )
    parser.add_argument(
        "--phone-number-id",
        default=os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""),
        help="Phone Number ID (أو من المتغير WHATSAPP_PHONE_NUMBER_ID)",
    )
    parser.add_argument(
        "--sender-name",
        default="",
        help="معلومة فقط: لا يمكن تغييره من السكربت",
    )
    parser.add_argument(
        "--sender-photo",
        default="",
        help="معلومة فقط: لا يمكن تغييرها من السكربت",
    )
    return parser.parse_args()


def send_whatsapp_text(token: str, phone_number_id: str, to_phone: str, text: str) -> dict[str, Any]:
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def prompt_if_missing(value: str, prompt_text: str) -> str:
    return value if value else input(prompt_text).strip()


def main() -> int:
    args = parse_args()

    if args.sender_name or args.sender_photo:
        print("تنبيه: اسم/صورة المرسل لا يمكن تعديلهما من السكربت، بل من إعدادات حساب الأعمال.")

    token = prompt_if_missing(args.token, "أدخل WHATSAPP_TOKEN: ")
    phone_number_id = prompt_if_missing(args.phone_number_id, "أدخل WHATSAPP_PHONE_NUMBER_ID: ")

    try:
        to_phone = normalize_phone(args.to)
    except ValueError as err:
        print(f"خطأ: {err}")
        return 1

    if not args.message.strip():
        print("خطأ: نص الرسالة لا يمكن أن يكون فارغًا")
        return 1

    if args.count < 1:
        print("خطأ: --count يجب أن يكون 1 أو أكثر")
        return 1

    if args.delay_seconds < 0:
        print("خطأ: --delay-seconds يجب أن يكون 0 أو أكثر")
        return 1

    for index in range(1, args.count + 1):
        try:
            result = send_whatsapp_text(token, phone_number_id, to_phone, args.message)
            print(f"تم إرسال الرسالة رقم {index}/{args.count} بنجاح")
            print(result)
        except urllib.error.HTTPError as err:
            body = err.read().decode("utf-8", errors="replace")
            print(f"فشل إرسال الرسالة رقم {index}: {body}")
            return 1
        except urllib.error.URLError as err:
            print(f"خطأ اتصال أثناء الرسالة رقم {index}: {err}")
            return 1

        if index < args.count and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)

    return 0


if __name__ == "__main__":
    sys.exit(main())
