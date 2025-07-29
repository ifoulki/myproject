<x-layoutAdm 
    page="الصفحة الشخصية"
    description="إنضم إلى عائلة تيفيناغ.كوم وساهم في الرقي بالمحتوى العربي في الأنترنيت بنشر مساهمتك في مجلتنا سواء كانت مقالات أو أخبار أو دروس ... إلخ. موقعنا يضم أيضا مكتبة كبيرة تحتوي على كتب متنوعة ومجالات وحتى مطبوعات مدرسية ونماذج اختبارات. نحن نرحب بأي مساهمة يمكن أن تفيد زوارنا."
>
    <article class="content">
        @if (session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif

            @php 
                $user = Auth::user();
                $images = array_filter(explode(',', $user->images));
            @endphp

            <ul class="list-group form">
                <li class="list-group-item">
                    @if (!empty($images))
                        <div id="imageCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
                            <div class="carousel-inner">
                                @foreach ($images as $index => $image)
                                    <div class="carousel-item {{ $index === 0 ? 'active' : '' }}">
                                        <img src="{{ asset('images/users/' . $image) }}" class="d-block w-100" alt="صورة {{ $user->Prenom }} {{ $user->Nom }}" style="max-width:400px; margin: auto;">
                                    </div>
                                @endforeach
                            </div>
                            <button class="carousel-control-prev" type="button" data-bs-target="#imageCarousel" data-bs-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">السابق</span>
                            </button>
                            <button class="carousel-control-next" type="button" data-bs-target="#imageCarousel" data-bs-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="visually-hidden">التالي</span>
                            </button>
                        </div>
                    @else
                        <div class="text-center mb-4">
                            <img src="{{ asset('assets/' . ($user->gender == 'Male' ? 'male.webp' : 'female.webp')) }}" class="img-fluid" alt="صورة {{ $user->Prenom }} {{ $user->Nom }}" style="max-width:400px;">
                        </div>
                    @endif
                </li>
                            <h1> {{ $user->name }}</h1>
            </ul>
                <b>الصفة :</b> {{ $user->role }}<hr>
                <b>البريد الإلكتروني :</b> {{ $user->email }}<hr>

                <a href="{{ route('users.edit', $user) }}" class="btn btn-primary">تعديل البيانات</a> <hr>

                @if ($user->role != 'admin')
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading">ملاحظة هامة!</h4>
                    <p>سيتمكن حسابك من النشر وإدارة المحتوى على الموقع بمجرد مراجعة حسابك من قبل إدارة الموقع.</p>
                    <hr>
                    <p class="mb-0">ندعوك للعودة لتسجيل الدخول إلى حسابك في وقت لاحق. نتطلع إلى تفعيل حسابك قريبًا، إن شاء الله.</p>
                </div>
            @else
                <ul>
                    <li><a href="{{ route('articles.index') }}">مراجعة المقالات</a></li>
                    <li><a href="{{ route('books.index') }}">مراجعة الكتب</a></li>
                    <li><a href="{{ route('videos.index') }}">مراجعة الفيديوهات</a></li>
                    <li><a href="{{ route('cours.index') }}">مراجعة القواميس البصرية</a></li>
                    <li><a href="{{ route('exams.index') }}">مراجعة الاختبارات</a></li>
                </ul>
            @endif

    </article>
</x-layoutAdm>