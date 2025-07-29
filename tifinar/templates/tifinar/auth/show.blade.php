<x-layoutAdm page='الصفحة الشخصية'>
    <section class="content">

        <div class="container">
            <div class="container">
                <h2 class="mb-4">عرض بيانات المستخدم</h2>

                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">معلومات المستخدم</h5>
                        <p class="card-text"><strong>اسم المستخدم:</strong> {{ $user->name }}</p>
                        <p class="card-text"><strong>البريد الإلكتروني:</strong> {{ $user->email }}</p>
                        <p class="card-text"><strong>الدور:</strong> {{ $user_role }}</p>
                        <p class="card-text"><strong>المستوى الدراسي:</strong> {{ $user->educational_level }}</p>

                        <a href="{{ route('user.edit', $user) }}" class="btn btn-primary">تعديل البيانات</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
</x-layoutAdm>