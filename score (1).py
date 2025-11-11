import os
import json
import joblib
import numpy as np
import pandas as pd
from azureml.core.model import Model

# ===============================
# 🔹 إعداد الأعمدة والمعلمات
# ===============================
NUMERICAL_FEATURE = 'المساحة'
CATEGORICAL_FEATURES = ['المنطقة', 'المدينة', 'المدينة / الحي', 'تصنيف العقار']
FINAL_MODEL_FEATURES = [NUMERICAL_FEATURE, 'المنطقة', 'المدينة', 'المدينة / الحي', 'تصنيف العقار', 'عدد العقارات']

# ===============================
# 🔹 المتغيرات العامة (تُملأ لاحقًا)
# ===============================
model = None
scaler = None
le_dict = None

# اسم النموذج المسجل في Azure ML
PRIMARY_MODEL_NAME = "real-estate-model-v1"

# ===============================
# 🔹 init() لتحميل الملفات
# ===============================
def init():
    global model, scaler, le_dict

    print("🚀 Initializing model assets...")

    try:
        try:
            model_root_path = Model.get_model_path(PRIMARY_MODEL_NAME)
            print(f"✅ Model loaded from Azure: {model_root_path}")
        except Exception:
            # التشغيل محلياً
            model_root_path = "Users/razankh445/model_folder"
            print(f"⚙️ Running locally — using path: {model_root_path}")

        # مسارات الملفات
        model_path = os.path.join(model_root_path, "real_estate_price_model3.pkl")
        scaler_path = os.path.join(model_root_path, "robust_scaler3.pkl")
        le_dict_path = os.path.join(model_root_path, "label_encoders.pkl")

        # التحقق من وجود الملفات
        for path in [model_path, scaler_path, le_dict_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"❌ File not found: {path}")

        # تحميل الملفات
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        le_dict = joblib.load(le_dict_path)

        print("✅ Model, Scaler, and LabelEncoders loaded successfully!")

    except Exception as e:
        print(f"🔥 FATAL ERROR in init(): {e}")
        raise


# ===============================
# 🔹 run() لتنفيذ التنبؤ
# ===============================
def run(raw_data):
    try:

        data_dict = json.loads(raw_data)
        input_data = data_dict if isinstance(data_dict, list) else data_dict.get('data', [])

        # إنشاء DataFrame من المدخلات
        input_features = [NUMERICAL_FEATURE, 'عدد العقارات'] + CATEGORICAL_FEATURES
        input_df = pd.DataFrame(input_data, columns=input_features)

        print("📊 Input DataFrame:")
        print(input_df)

        # ترميز الخصائص الفئوية
        df_processed = input_df.copy()
        for col in CATEGORICAL_FEATURES:
            df_processed[col] = le_dict[col].transform(df_processed[col].astype(str))

        # تطبيق الـ RobustScaler
        df_processed[NUMERICAL_FEATURE] = scaler.transform(df_processed[[NUMERICAL_FEATURE]])

        # ترتيب الأعمدة حسب ما تدرب عليه النموذج
        final_input = df_processed[FINAL_MODEL_FEATURES]

        print("✅ Processed Input:")
        print(final_input)

        # تنبؤ السعر (log)
        preds_log = model.predict(final_input)

        # تحويل القيم إلى نطاقها الأصلي
        preds = np.expm1(preds_log)

        print("💰 Predicted Prices:", preds.tolist())

        return json.dumps(preds.tolist())

    except Exception as e:
        print(f"⚠️ Prediction failed: {e}")
        return json.dumps({"error": str(e)})


# ===============================
# 🔹 اختبار محلي
# ===============================
if __name__ == "__main__":
    init()
    print("\n✅ Score.py initialized successfully!\n")

    sample_data = [
      {
            "المساحة": 250,
            "عدد العقارات": 1,
            "المنطقة": "منطقة الرياض",
            "المدينة": "الرياض",
            "المدينة / الحي": "الرياض/نمار",
            "تصنيف العقار": "سكني"
        }
    ]

    result = run(json.dumps(sample_data))
    print("\n🎯 Final Prediction Output:")
    print(result)
