import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from tifinar.models import VisitorsIp, Visitors

# إعدادات الرسوم البيانية
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 24,
    'axes.titlesize': 28,
    'axes.labelsize': 26,
    'xtick.labelsize': 22,
    'ytick.labelsize': 22,
    'legend.fontsize': 22,
    'figure.titlesize': 30,
    'figure.dpi': 150,
    'figure.figsize': (22, 14),
    'axes.grid': True,
    'grid.alpha': 0.3,
})

def reshape_arabic(text):
    """إعادة تشكيل النصوص العربية للعرض الصحيح"""
    try:
        reshaped_text = reshape(text)
        return get_display(reshaped_text)
    except:
        return text

def generate_chart(fig):
    """تحويل الرسم البياني إلى صورة base64"""
    buffer = BytesIO()
    try:
        fig.savefig(
            buffer,
            format='png',
            dpi=150,
            bbox_inches='tight',
            facecolor='white',
            transparent=False
        )
        plt.close(fig)
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error generating chart: {e}")
        return ""
    finally:
        buffer.close()

@login_required
def dashboard_view(request):
    """لوحة التحكم الرئيسية"""
    # عناوين الرسوم البيانية
    titles = {
        'ip': reshape_arabic('توزيع الزيارات حسب عنوان IP'),
        'device': reshape_arabic('نوع الأجهزة المستخدمة'),
        'daily': reshape_arabic('الزيارات خلال أسبوع'),
        'pages': reshape_arabic('أكثر الصفحات زيارة'),
        'y_label': reshape_arabic('عدد الزيارات'),
        'x_label_ip': reshape_arabic('عنوان IP'),
        'x_label_date': reshape_arabic('التاريخ'),
        'x_label_page': reshape_arabic('الصفحة')
    }

    # 1. إحصائيات عناوين IP
    ip_chart = ""
    try:
        ip_data = VisitorsIp.objects.values('ip').annotate(
            visits=Sum('number_of_visits')
        ).order_by('-visits')[:10]
        
        if ip_data.exists():
            df_ip = pd.DataFrame(list(ip_data))
            fig, ax = plt.subplots(figsize=(20, 10))
            sns.barplot(x='ip', y='visits', data=df_ip, palette='Blues_d')
            
            ax.set_title(titles['ip'], fontsize=28, pad=20)
            ax.set_ylabel(titles['y_label'], fontsize=24)
            ax.set_xlabel(titles['x_label_ip'], fontsize=24)
            plt.xticks(rotation=45)
            plt.tight_layout()
            ip_chart = generate_chart(fig)
    except Exception as e:
        print(f"IP Chart Error: {e}")

    # 2. إحصائيات نوع الجهاز
    device_chart = ""
    try:
        device_data = VisitorsIp.objects.values('device_type').annotate(
            visits=Sum('number_of_visits')
        ).order_by('-visits')
        
        if device_data.exists():
            df_device = pd.DataFrame(list(device_data))
            fig, ax = plt.subplots(figsize=(16, 16))
            df_device['device_type'] = df_device['device_type'].fillna('غير معروف')
            
            ax.pie(
                df_device['visits'],
                labels=df_device['device_type'],
                autopct='%1.1f%%',
                textprops={'fontsize': 20},
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
            )
            
            ax.set_title(titles['device'], fontsize=28, pad=20)
            plt.tight_layout()
            device_chart = generate_chart(fig)
    except Exception as e:
        print(f"Device Chart Error: {e}")

    # 3. إحصائيات الزيارات اليومية
    daily_chart = ""
    try:
        date_from = timezone.now() - timedelta(days=7)
        daily_data = VisitorsIp.objects.filter(
            visit_timestamp__gte=date_from
        ).extra({'date': "DATE(visit_timestamp)"}).values('date').annotate(
            visits=Sum('number_of_visits')
        ).order_by('date')
        
        fig, ax = plt.subplots(figsize=(20, 10))
        
        if daily_data.exists():
            df_daily = pd.DataFrame(list(daily_data))
            sns.lineplot(x='date', y='visits', data=df_daily, marker='o', markersize=10)
        else:
            # إنشاء بيانات افتراضية إذا لم توجد بيانات
            dates = pd.date_range(end=timezone.now().date(), periods=7)
            df_daily = pd.DataFrame({'date': dates, 'visits': [0]*7})
            sns.lineplot(x='date', y='visits', data=df_daily, marker='o', markersize=10)
        
        ax.set_title(titles['daily'], fontsize=28, pad=20)
        ax.set_ylabel(titles['y_label'], fontsize=24)
        ax.set_xlabel(titles['x_label_date'], fontsize=24)
        plt.xticks(rotation=45)
        plt.tight_layout()
        daily_chart = generate_chart(fig)
    except Exception as e:
        print(f"Daily Chart Error: {e}")

    # 4. إحصائيات الصفحات
    pages_chart = ""
    try:
        pages_data = Visitors.objects.values('title').annotate(
            visits=Count('id')
        ).order_by('-visits')[:5]
        
        if pages_data.exists():
            df_pages = pd.DataFrame(list(pages_data))
            df_pages['title'] = df_pages['title'].fillna('غير معروف').apply(reshape_arabic)
            
            fig, ax = plt.subplots(figsize=(20, 10))
            sns.barplot(x='title', y='visits', data=df_pages, palette='Purples_r')
            
            ax.set_title(titles['pages'], fontsize=28, pad=20)
            ax.set_ylabel(titles['y_label'], fontsize=24)
            ax.set_xlabel(titles['x_label_page'], fontsize=24)
            plt.xticks(rotation=45)
            plt.tight_layout()
            pages_chart = generate_chart(fig)
    except Exception as e:
        print(f"Pages Chart Error: {e}")

    context = {
        'ip_chart': ip_chart,
        'device_chart': device_chart,
        'daily_chart': daily_chart,
        'page_chart': pages_chart,
        'last_update': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render(request, 'tifinar/auth/dashboard.html', context)