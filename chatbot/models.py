from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Course(models.Model):
    class TypeInCourse(models.TextChoices):
        GENERAL = "GEN", _("通識課程")
        EDUCATION = "EDU", _("教育學程")
        PE_SOPHOMORE = "PSS", _("大二體育")
        PE_JUNIOR_SENIOR = "PJS", _("大三四體育")
        LANGUAGE = "LAN", _("精進中英外文")
        MILITARY = "MIL", _("軍訓")
        # DEPARTMENT = "DEP", _("系課程")
        
    course_type = models.CharField(
        max_length=3,
        choices=TypeInCourse,
        verbose_name="類型",
        default=TypeInCourse.GENERAL,
    )
    
    course_name = models.CharField(
        max_length=20, 
        verbose_name="課名", 
        help_text="以教務系統顯示的全名為主"
    )
    
    teacher_name = models.CharField(
        max_length=20,
        verbose_name="老師/【合開】",
        help_text="【合開】連【】也要記得輸進去哦！",
    )
    
    submitter_name = models.CharField(
        max_length=15, 
        default="匿名", 
        verbose_name="投稿者", 
        help_text="不口以超過15字"
    )

    feedback_content = models.TextField(
        verbose_name="內容"
    )

    evaluation_semester = models.CharField(
        max_length=5,
        default="113-1",
    )

    last_updated_time = models.DateTimeField(
        auto_now=True, 
        verbose_name="上次修改日期"
    )
    def __str__(self):
        return self.course_name