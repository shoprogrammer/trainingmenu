from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
   
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):             
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
GENDER_CHOICE = [(None,"--"),("m","男性"),("f","女性")]

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,verbose_name="ユーザー名")
    affiliation = models.CharField(max_length=100,default="未設定",verbose_name="所属")
    height = models.IntegerField(default=170,verbose_name="身長")
    weight = models.IntegerField(default=70,verbose_name="体重")
    total_score = models.IntegerField(default=500,verbose_name="合計重量")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICE,default='m',verbose_name="性別")
    birthday = models.DateField(default="2020-01-01",verbose_name="生年月日")
    #tuika
    gl_point = models.FloatField(default=0.0, verbose_name="GLポイント")

    def __str__(self):
        return self.username
    #tuika
    def calculate_gl_point(self):
        """GLポイントを計算する関数"""
        if self.gender == 'm':
            a, b, c  = 1199.72839, 1025.18162, -0.00921
            denominator = a - b ** (c * self.weight)
        elif self.gender == 'f':
            a, b, c = 610.32796, 1045.59282, -0.03048
            denominator = a - b ** (c * self.weight)
        else:
            return 0  # 性別が設定されていない場合は0を返す
        
        
        if denominator == 0:
            return 0  # 0除算を回避
        
        gl_point = (100 * self.total_score) / denominator
        return round(gl_point, 2)  # 小数点2位まで丸める

    def save(self, *args, **kwargs):
        """保存する際にGLポイントを再計算"""
        self.gl_point = self.calculate_gl_point()
        super().save(*args, **kwargs)  # 元のsaveメソッドを呼び出す


def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.username = instance.email
        profile_obj.gl_point = profile_obj.calculate_gl_point() 
        profile_obj.save()

post_save.connect(post_user_created, sender=User)