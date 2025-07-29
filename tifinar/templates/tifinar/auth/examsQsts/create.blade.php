<x-layoutAdm page="إضافة سؤال">

    <section class="content">

        <h1><i class="fas fa-edit"></i> إضافة سؤال:</h1>
        @if ($errors->has('general'))
            <div class="error-feedback">
                <i class="fas fa-exclamation-circle"></i> {{ $errors->first('general') }}
            </div>
        @endif

    
        <form style="width: 100%" class="form" method="POST" action="{{ route('examItems.store') }}" enctype="multipart/form-data">

            @csrf

            <div class="form">
                <label class="label"><i class="fas fa-clipboard-list"></i> السؤال تابع للاختبار رقم:</label>
                <input class="small-input @error('exam_id') is-invalid @enderror" type="number" name="exam_id" id="exam_id" 
                    value="{{ old('exam_id', \App\Models\Exam::max('exam_id')) }}">
                @error('exam_id')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            
            <hr>
            
            <div class="form">
                <label class="label"><i class="fas fa-hashtag"></i> رقم السؤال:</label>
                <input title="لا يمكن تغيير رقم، سيضع النظام الرقم المناسب تلقائيا" readonly class="@error('qsts_id') is-invalid @enderror small-input" type="number" name="qsts_id" id="qsts_id" value="{{ $nextQstsId }}">
                @error('qsts_id')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            
            <hr>
            
            <div class="form">
                <label class="label"><i class="fas fa-language"></i> بأي لغة ستطرح السؤال؟</label>
                <select class="small-input @error('dir') is-invalid @enderror" name="dir">
                    <option value="" disabled selected>اختر اللغة</option>
                    <option value="rtl" {{ old('dir') === 'rtl' ? 'selected' : '' }}>العربية</option>
                    <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>Français</option>
                    <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>English</option>
                </select>
                @error('dir')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            
            <hr>

            <div class="form">
                <label class="label"><i class="fas fa-star"></i> السؤال عليه:</label>
                <select class="small-input @error('mark') is-invalid @enderror" name="mark">
                    <option value="" disabled selected>كم نقطة ؟</option>
                    @for ($i = 0.5; $i <= 5; $i += 0.5)
                        <option value="{{ $i }}" {{ old('mark') == $i ? 'selected' : '' }}>{{ $i }} نقطة</option>
                    @endfor
                </select>
                @error('mark')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            
            <hr>

            <div class="form">
                <label class="label"><i class="fas fa-pen"></i> السطر الأول للسؤال:</label>
                <textarea name="qst_1st_line" class="@error('qst_1st_line') is-invalid @enderror" placeholder="نص السؤال...">{{ old('qst_1st_line') }}</textarea>
                @error('qst_1st_line')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            
            <hr>
            
            <div class="form">
                <label class="label"><i class="fas fa-pen"></i> السطر الثاني للسؤال:</label>
                <textarea name="qsts" placeholder="نص السؤال...">{{ old('qsts') }}</textarea>
            </div>
            @error('qsts')
                <small class="text-danger">{{ $message }}</small>
            @enderror

            <hr>

            <div class="form">
                <label class="label"><i class="fas fa-question-circle"></i> شكل السؤال:</label>
                <select class="small-input the_type @error('the_type') is-invalid @enderror" name="the_type" >
                    <option value="" disabled selected> حدد الشكل </option>
                    <option value="radio" {{ old('the_type') === 'radio' ? 'selected' : '' }}>اختيارات (واحد فقط صحيح)</option>
                    <option value="checkbox" {{ old('the_type') === 'checkbox' ? 'selected' : '' }}>اختيارات (واحد أو أكثر صحيح)</option>
                    <option value="text" {{ old('the_type') === 'text' ? 'selected' : '' }}>إجابة قصيرة</option>
                    <option value="textarea" {{ old('the_type') === 'textarea' ? 'selected' : '' }}>إجابة طويلة</option>
                </select>
                @error('the_type')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="form answerField">
                <label class="label"><i class="fas fa-check-circle"></i> الإجابة الصحيحة:</label>
                <textarea class="@error('correct_answer') is-invalid @enderror" name="correct_answer" placeholder="أكتب الإجابة الصحيحة هنا...">{{ old('correct_answer') }}</textarea>
                @error('correct_answer')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>   

            <p class="for_radio">باقي الاختيارات خاطئة :</p>

            <div class="form choiceFields">
                <div>
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الأول:</label>
                    <input class="input choicetext" type="text" name="choice1[]" placeholder="أدخل النص هنا..." value="{{ old('choice1.0') }}">
                    <select class="small-input key choiceKey" name="choice1[]">
                        <option value="" disabled {{ old('choice1.1') === null ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option class="wrong" value="false" {{ old('choice1.1') === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option class="correct" value="true" {{ old('choice1.1') === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                    @error('choice1*')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div>
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الثاني:</label>
                    <input class="input choicetext" type="text" name="choice2[]" placeholder="أدخل النص هنا..." value="{{ old('choice2.0') }}">
                    <select class="small-input key choiceKey" name="choice2[]">
                        <option value="" disabled {{ old('choice2.1') === null ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option class="wrong" value="false" {{ old('choice2.1') === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option value="true" {{ old('choice2.1') === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                    @error('choice2*')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div >
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الثالث:</label>
                    <input class="input choicetext" type="text" name="choice3[]" placeholder="أدخل النص هنا..." value="{{ old('choice3.0') }}">
                    <select class="small-input key choiceKey" name="choice3[]">
                        <option value="" disabled {{ old('choice3.1') === null ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option value="false" {{ old('choice3.1') === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option value="true" {{ old('choice3.1') === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                    @error('choice3*')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>
            </div>

            <hr>

            <div>
                <label class="label"><i class="fas fa-image"></i> صورة تظهر أسفل السؤال:</label>
                <input type="file" name="qst_img" class="form-control" onchange="previewImage(this, 'qst_img_preview')">
                <img id="qst_img_preview" style="display:none; max-width: 200px; margin-top: 10px;">
            </div>
            @error('qst_img')
                <small class="text-danger">{{ $message }}</small>
            @enderror

            <hr>

            <label class="label"><i class="fas fa-comment-dots"></i> رسالة تظهر عندما تكون الإجابة صحيحة:</label><br>
            <textarea name='if_choising_correct' placeholder='أكتب رسالة تظهر عندما تكون الإجابة صحيحة ...'>{{ old('if_choising_correct') }}</textarea>
            @error('if_choising_correct')
                <small class="text-danger">{{ $message }}</small>
            @enderror

            <label class="label"><i class="fas fa-image"></i> صورة تظهر إذا كانت الإجابة صحيحة:</label>
            <input class="form-control" type="file" name="img_if_right_answer" onchange="previewImage(this, 'img_if_right_preview')">
            <img id="img_if_right_preview" style="display:none; max-width: 200px; margin-top: 10px;">
            @error('img_if_right_answer')
                <small class="text-danger">{{ $message }}</small>
            @enderror
        </div>

        <hr>

        <div class="form">
            <label class="label"><i class="fas fa-comment-dots"></i> رسالة تظهر عندما تكون الإجابة خاطئة:</label><br>
            <textarea name='if_its_wrong_answer' placeholder='أكتب رسالة تظهر عندما تكون الإجابة خاطئة ...'>{{ old('if_its_wrong_answer') }}</textarea>
            @error('if_its_wrong_answer')
                <small class="text-danger">{{ $message }}</small>
            @enderror

            <label class="label"><i class="fas fa-image"></i> صورة تظهر إذا كانت الإجابة خاطئة:</label>
            <input class="form-control" type="file" name="img_if_wrong_answer" onchange="previewImage(this, 'img_if_wrong_preview')">
            <img id="img_if_wrong_preview" style="display:none; max-width: 200px; margin-top: 10px;">
            @error('img_if_wrong_answer')
                <small class="text-danger">{{ $message }}</small>
            @enderror
        </div>

            <div class="form">
                <div class="text-center">
                    <button type="submit" class="btn btn-success"><i class="fas fa-plus"></i> إضافة السؤال</button>
                </div>
            </div>
        </form>
    </section>

    <script>

        function previewImage(input, previewId) {
            const preview = document.getElementById(previewId);
            const file = input.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            } else {
                preview.style.display = 'none';
            }
        }

        document.getElementById('exam_id').addEventListener('change', function() {
            const examId = this.value;
            
            if (examId) {
                fetch('/get-next-qsts-id?exam_id=' + examId)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('qsts_id').value = data.next_qsts_id;
                        } else {
                            console.error('No valid response');
                        }
                    })
                    .catch(error => console.error('Error fetching data:', error));
            }
        });

        document.addEventListener("DOMContentLoaded", function () {
    const the_type = document.querySelector(".the_type");
    const choiceFields = document.querySelectorAll(".choiceFields");
    const answerField = document.querySelectorAll(".answerField");
    const choicetext = document.querySelectorAll(".choicetext");
    const choiceKey = document.querySelectorAll(".choiceKey");
    const for_radio = document.querySelectorAll(".for_radio");

    function updateVisibility() {
        const Type = the_type.value;

        if (Type === "radio") {
            choicetext.forEach(el => el.style.display = "block");
            choiceKey.forEach(el => el.style.display = "none");
            answerField.forEach(el => el.style.display = "block");
            for_radio.forEach(el => el.style.display = "block");
            choiceFields.forEach(el => el.style.display = "block");

        } else if (Type === "checkbox") {
            choicetext.forEach(el => el.style.display = "block");
            choiceKey.forEach(el => el.style.display = "block");
            answerField.forEach(el => el.style.display = "none");
            choiceFields.forEach(el => el.style.display = "block");
            for_radio.forEach(el => el.style.display = "none");


        } else {
            choicetext.forEach(el => el.style.display = "none");
            choiceKey.forEach(el => el.style.display = "none");
            answerField.forEach(el => el.style.display = "block");
            choiceFields.forEach(el => el.style.display = "none");
            for_radio.forEach(el => el.style.display = "none");

        }
    }

    the_type.addEventListener("change", updateVisibility);
    updateVisibility();
});
</script>
    
    
</x-layoutAdm>
