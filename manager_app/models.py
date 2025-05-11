from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    COLORS = (
        ('#808080', '灰色'),
        ('#ff6961', '赤色'),
        ('#ffb480', '橙色'),
        ('#f8f38d', '黄色'),
        ('#42d6a4', '緑色'),
        ('#08cad1', '水色'),
        ('#59adf6', '青色'),
        ('#9d94ff', '紫色'),
        ('#c780e8', '桃色'),
    )
    TYPE = (
        ('管理', '管理'),
        ('教练', '教练'),
        ('其他', '其他'),
    )
    SKI = (
        ('双板0极', '双板0极'),
        ('双板1级', '双板1级'),
        ('双板2级', '双板2级'),
        ('双板3级', '双板3级'),
        ('双板4级', '双板4级'),
    )
    SNOWBOARD = (
        ('单板0极', '单板0极'),
        ('单板1级', '单板1级'),
        ('单板2级', '单板2级'),
        ('单板3级', '单板3级'),
        ('单板4级', '单板4级'),
    )
    SKI_SYSTEM = (
        ('加拿大', '加拿大'),
        ('新西兰', '新西兰'),
        ('澳洲', '澳洲'),
        ('日本', '日本'),
        ('其他', '其他'),
        ('无', '无'),
    )
    SNOWBOARD_SYSTEM = (
        ('加拿大', '加拿大'),
        ('新西兰', '新西兰'),
        ('澳洲', '澳洲'),
        ('日本', '日本'),
        ('其他', '其他'),
        ('无', '无'),
    )
    YEAR_CHOICES = (
        ('1年', '1年'),
        ('2年', '2年'),
        ('3年', '3年'),
        ('4年', '4年'),
        ('5年以上', '5年以上'),
    )
    FARE_PECENTAGE = (
        ('20', '20'),
        ('21.5', '21.5'),
        ('23', '23'),
        ('24.5', '24.5'),
        ('26', '26'),
        
        ('30', '30'),
        ('31.5', '31.5'),
        ('33', '33'),
        ('34.5', '34.5'),
        ('36', '36'),
        
        ('40', '40'),
        ('41.5', '41.5'),
        ('43', '43'),
        ('44.5', '44.5'),
        ('46', '46'),
    )
    FULL_ATTENDANCE = (
        ('3', '3'),
        ('0', '0'),
    )
    CUSTOMERS_EVALUATION = (
        ('2', '2'),
        ('0', '0'),
    )
    COMPANY_EVALUATION = (
        ('5', '5'),
        ('0', '0'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField("生年月日", blank=True, null=True)
    color = models.CharField("教练色", max_length=30, choices=COLORS)
    contract_type = models.CharField("职务", max_length=50, choices=TYPE, default='教练')
    fullname = models.CharField("姓名", max_length=20, blank=True)
    phone = models.CharField("電話", max_length=20, blank=True)
    email = models.CharField("邮箱", max_length=50, blank=True)
    wechat = models.CharField("微信", max_length=20, blank=True)
    whatsapp = models.CharField("Whatsapp", max_length=20, blank=True)
    line = models.CharField("LINE", max_length=20, blank=True)
    ski_system = models.CharField("双板体系", max_length=50, choices=SKI_SYSTEM, default='加拿大')
    snowboard_system = models.CharField("单板体系", max_length=50, choices=SNOWBOARD_SYSTEM, default='加拿大')
    ski = models.CharField("级别", max_length=50, choices=SKI, default='双板1级')
    snowboard = models.CharField("级别", max_length=50, choices=SNOWBOARD, default='单板1级')
    accommodation = models.CharField("宿舍", max_length=20, blank=True)
    years_choices = models.CharField("経験年数", choices=YEAR_CHOICES, default='1年')
    fare_percentage = models.CharField("提成比率", max_length=50, choices=FARE_PECENTAGE, default='20')
    full_attendance = models.CharField("全勤提成", max_length=50, choices=FULL_ATTENDANCE, default='3')
    customers_evaluation = models.CharField("客人評価", max_length=50, choices=CUSTOMERS_EVALUATION, default='2')
    company_evaluation = models.CharField("公司評価", max_length=50, choices=COMPANY_EVALUATION, default='5')
    note = models.CharField("備考", max_length=500, blank=True)
    is_active = models.BooleanField("現役中", default=True)
    date_created = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f"{self.fullname}"
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Lesson(models.Model):
    PAYMENT_TYPES = (
        ('現金','現金'),
        ('刷卡', '刷卡'),
        ('電子支付', '電子支付'),
        ('未支付', '未支付'),
    )
    PLACE = (
        ('比洛夫', '比洛夫'),
        ('花园', '花园'),
        ('安努', '安努'),
        ('莫伊哇', '莫伊哇'),
        ('留寿都', '留寿都'),
        ('喜乐乐', '喜乐乐'),
        ('其他', '其他'),
    )
    LESSON_TYPE = (
        ('初学', '初学'),
        ('初级', '初级'),
        ('中级', '中级'),
        ('上级', '上级'),
        ('导滑', '导滑'),
    )

    lesson_number = models.IntegerField("课次", blank=False, null=True, default=0)
    instructors = models.ManyToManyField(Profile, related_name="instructors", blank=False)
    client = models.CharField("客人姓名", max_length=255)
    lesson_type = models.CharField("课程类型", max_length=50, choices=LESSON_TYPE, default='初学')
    address = models.CharField("酒店", max_length=255)
    place = models.CharField("雪场", max_length=50, choices=PLACE, default='比洛夫')
    payment_type = models.CharField("付款方式", max_length=50, choices=PAYMENT_TYPES, default='未支付')
    payment_amount = models.DecimalField("付款金額", max_digits=10, decimal_places=2, blank=True, null=True)
    payment_date = models.DateTimeField("付款日", blank=True, null=True)
    note = models.CharField("備考", max_length=255, blank=True, null=True)
    start_date = models.DateTimeField("開始日")
    end_date = models.DateTimeField("終了日")
    start_time = models.TimeField("開始時間", blank=True, null=True)
    end_time = models.TimeField("終了時間", blank=True, null=True)
    finished = models.BooleanField("終了", default=False)
    date_created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return f"{self.lesson_number} - {self.client} - {self.instructors.all()}"
    
    @property
    def Is_past(self):
        today = date.today()
        if self.end_date.date() < today:
            text = "Past"
        else:
            text = "Future"
        return text

class Notification(models.Model):
    author = models.ForeignKey(User, related_name="notification", on_delete=models.CASCADE)
    content = models.CharField("内容", max_length=500)
    date_created = models.DateTimeField("作成日", auto_now_add=True)
    
    def __str__(self):
        return f"{self.content} - {self.author} - {self.date_created}"
    