<ul class="comments-list">
    @if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
    @endif

    <h2>عدد التعليقات: {{ $exam->comments->count() }}</h2>

    @foreach($exam->comments as $comment)
    @php
    $backgroundColor = '';
    $borderColor = '';
    $inputBackgroundColor = '';

    switch ($comment->visibility_status) {
        case 'public':
            $backgroundColor = '#e7ffe7'; // أخضر فاتح
            $borderColor = '#4CAF50'; // أخضر داكن
            $inputBackgroundColor = '#f0fff0'; // خلفية المدخلات (أخضر فاتح جداً)
            break;
        case 'under_review':
            $backgroundColor = '#fff9c4'; // أصفر فاتح
            $borderColor = '#FFC107'; // أصفر داكن
            $inputBackgroundColor = '#fffde7'; // خلفية المدخلات (أصفر فاتح جداً)
            break;
        case 'restricted':
            $backgroundColor = '#ffe0e0'; // أحمر فاتح
            $borderColor = '#F44336'; // أحمر داكن
            $inputBackgroundColor = '#ffebee'; // خلفية المدخلات (أحمر فاتح جداً، لكن أفتح قليلاً)
            break;
    }
    @endphp

    <li class="comment-item">
        <form style="border: solid 2px {{$borderColor}}; padding:10px; background:{{$backgroundColor}}" action="{{ route('comments.update', ['comment' => $comment->cmt_id]) }}" method="POST" class="comment-form">
            @csrf
            @method('PUT')

            <input type="hidden" name="page_title" value="{{ $exam->title }}">

            <div class="form-group">
                <label for="author_name"><i class="fas fa-user"></i> اسمك:</label>
                <input style="background-color: {{ $inputBackgroundColor }};" value="{{ $comment->author_name ?? '' }}" type="text" id="author_name" name="author_name" required>
            </div>

            <div class="form-group">
                <label for="author_email"><i class="fas fa-envelope"></i> بريدك الإلكتروني:</label>
                <input style="background-color: {{ $inputBackgroundColor }};" value="{{ $comment->author_email ?? '' }}" type="email" id="author_email" name="author_email" required>
            </div>

            <div class="form-group">
                <label for="cmt_subject"><i class="fas fa-comment-alt"></i> التعليق:</label>
                <textarea style="background-color: {{ $inputBackgroundColor }};" id="cmt_subject" name="cmt_subject" rows="4" required>{{ $comment->cmt_subject }}</textarea>
            </div>

            <div class="form-group">
                <label>الحالة:</label>
                <div style="display: flex; gap: 15px; font-size: 1.2em;">
                    <label>
                        <input type="radio" name="visibility_status" value="public" {{ $comment->visibility_status == 'public' ? 'checked' : '' }} onchange="updateStatusColor(this)"> 
                        <span style="color: #4CAF50;"><i class="fas fa-globe"></i> عام</span>
                    </label>
                    <label>
                        <input type="radio" name="visibility_status" value="under_review" {{ $comment->visibility_status == 'under_review' ? 'checked' : '' }} onchange="updateStatusColor(this)"> 
                        <span style="color: #FFC107;"><i class="fas fa-eye-slash"></i> قيد المراجعة</span>
                    </label>
                    <label>
                        <input type="radio" name="visibility_status" value="restricted" {{ $comment->visibility_status == 'restricted' ? 'checked' : '' }} onchange="updateStatusColor(this)"> 
                        <span style="color: #F44336;"><i class="fas fa-lock"></i> مقيد</span>
                    </label>
                </div>
            </div>

            <button type="submit" class="review-btn" style="background: {{$borderColor}}; color: white;">
                <i class="fas fa-check-circle"></i> تمت مراجعة التعليق
            </button>
        </form>
        <hr>
    </li>
    @endforeach
</ul>

<!-- SweetAlert2 JS -->
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.js"></script>

<script>
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // منع الإرسال الفوري

            Swal.fire({
                title: 'هل أنت متأكد؟',
                text: "هل تريد تعديل هذا التعليق؟",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'نعم، تعديل!',
                cancelButtonText: 'لا، إلغاء'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit(); // إرسال النموذج إذا تم التأكيد
                }
            });
        });
    });

    function updateStatusColor(radio) {
        let form = radio.closest('form');
        let inputBackgroundColor = '';

        switch (radio.value) {
            case 'public':
                inputBackgroundColor = '#f0fff0'; // أخضر فاتح جداً
                break;
            case 'under_review':
                inputBackgroundColor = '#fffde7'; // أصفر فاتح جداً
                break;
            case 'restricted':
                inputBackgroundColor = '#ffebee'; // أحمر فاتح جداً
                break;
        }

        form.querySelectorAll('input[type="text"], input[type="email"], textarea').forEach(input => {
            input.style.backgroundColor = inputBackgroundColor;
        });
    }
</script>

