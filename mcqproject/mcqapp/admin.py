from django.contrib import admin
from .models import  QuizResult  # Import the Quiz and QuizResult models
from django.contrib import admin
from .models import QuizResult, QuestionAttempt, UserProfile, UploadedFile, EmailVerification




class QuestionAttemptInline(admin.TabularInline):
    model = QuestionAttempt
    extra = 0
    readonly_fields = ('question', 'user_answer', 'correct_answer', 'is_correct', 'time_taken')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz_name', 'score', 'total_questions', 'percentage', 'time_taken', 'difficulty', 'created_at')
    list_filter = ('user', 'difficulty', 'created_at')
    search_fields = ('user__username', 'quiz_name')
    ordering = ('-created_at',)
    inlines = [QuestionAttemptInline]
    
    fieldsets = (
        ('Quiz Information', {
            'fields': ('user', 'quiz_name', 'created_at')
        }),
        ('Results', {
            'fields': ('score', 'total_questions', 'percentage', 'time_taken', 'difficulty', 'time_efficiency')
        }),
    )
    
    readonly_fields = ('created_at',)

@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz_attempt', 'short_question', 'user_answer', 'correct_answer', 'is_correct', 'time_taken')
    list_filter = ('quiz_attempt__user', 'is_correct')
    search_fields = ('question', 'user_answer', 'correct_answer')
    
    def short_question(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    short_question.short_description = 'Question'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'otp_created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'num_questions', 'difficulty', 'created_at')
    list_filter = ('difficulty', 'created_at')

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'expiration_time')
    search_fields = ('user__username', 'verification_code')