from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class BaseLessonSerializer(serializers.ModelSerializer):
    """Base lesson serializer with the shared ``validate()`` — single group
    currency + participant count vs lesson type. Reused by the admin and
    teacher-cabinet serializers (the read-only student one doesn't need it)."""

    def validate(self, attrs):
        students = attrs.get("students")
        if students is None and self.instance is not None:
            students = list(self.instance.students.all())
        students = students or []
        lesson_type = attrs.get("lesson_type", getattr(self.instance, "lesson_type", None))

        if students:
            if len({student.currency_id for student in students}) > 1:
                raise serializers.ValidationError(
                    {"students": _("All students must have one currency.")}
                )

        if lesson_type is not None and students:
            count = len(students)
            if (lesson_type.min_participants is None
                    and lesson_type.max_participants is None and count != 1):
                raise serializers.ValidationError({"students": _("Must be exactly 1 student.")})
            if lesson_type.min_participants and count < lesson_type.min_participants:
                raise serializers.ValidationError(
                    {"students": _("Min students: {n}.").format(n=lesson_type.min_participants)})
            if lesson_type.max_participants and count > lesson_type.max_participants:
                raise serializers.ValidationError(
                    {"students": _("Max students: {n}.").format(n=lesson_type.max_participants)})
        return attrs
