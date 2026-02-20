# FAKE-SPAM

## WhatsApp Auto Sender (Official API)

الأداة ترسل تلقائيًا عبر **WhatsApp Cloud API الرسمي**.

- الرقم الافتراضي: `+9647734549509`
- نص الرسالة الافتراضي: `السلام علييكم`
- عدد الرسائل الافتراضي: `3`

> ملاحظة: اسم وصورة المرسل لا يمكن تغييرهما من السكربت؛ يتم ضبطهما من إعدادات WhatsApp Business في Meta.

## المتطلبات

- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`

## تشغيل سريع (بنفس طلبك)

```bash
export WHATSAPP_TOKEN="YOUR_TOKEN"
export WHATSAPP_PHONE_NUMBER_ID="YOUR_PHONE_NUMBER_ID"
python3 whatsapp_sender.py
```

الأمر السابق سيرسل 3 رسائل متتالية تلقائيًا إلى الرقم الافتراضي بالنص الافتراضي.

## تخصيص القيم

```bash
python3 whatsapp_sender.py \
  --to +9647734549509 \
  -m "السلام علييكم" \
  --count 3 \
  --delay-seconds 0.5
```
