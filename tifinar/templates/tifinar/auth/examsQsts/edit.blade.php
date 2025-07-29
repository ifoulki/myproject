<x-layoutAdm page='تعديل سؤال'>

    <section class="content" >

        <h1><i class="fas fa-edit"></i> تعديل سؤال:</h1>

            <form style="width: 100%" class="form" method="POST" action="{{ route('examItems.update', $ExamItems->premary_id) }}" enctype="multipart/form-data">

                @csrf
                @method('PUT')

                <div class="form" >
                    <label class="label"> السؤال تابع للإختبار رقم :</label>
                    <input required class="small-input" type="number" name="exam_number" value="{{ $ExamItems->exam_number }}">
                </div>

                <div class="form" >
                    <label class="label"> رقم السؤال :</label>
                    <input required class="small-input" type="number" name="qsts_id" value="{{ $ExamItems->qsts_id }}">
                </div>

                <hr>

                <div class="form" >
                    <label class="label"> السؤال عليه:</label>
                    <select class="small-input" name="mark">
                        <option value="" disabled selected>كم نقطة؟</option>
                        @foreach ([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5] as $mark)
                            @php
                                if ($mark == 1){
                                    $text="نقطة";
                                }elseif ($mark == 2){
                                    $text="نقطتين";
                                }elseif ($mark == 0.5){
                                    $text="نصف نقطة";
                                }else{
                                    $text="$mark نقاط";
                                }
                            @endphp
                            <option value="{{ $mark }}" {{ $ExamItems->mark == $mark ? 'selected' : '' }}>{{$text}}</option>
                        @endforeach
                    </select>
                </div>
                <hr>

                <div class="form" >
                    <label class="label"> بأي لغة ستطرح السؤال ؟</label>
                    <select class="small-input" name="dir">
                        <option value="" disabled selected>اختر اللغة</option>
                        <option value="rtl" {{ $ExamItems->dir === 'rtl' ? 'selected' : '' }}>العربية</option>
                        <option value="ltr" {{ $ExamItems->dir === 'ltr' ? 'selected' : '' }}>Français</option>
                        <option value="ltr" {{ $ExamItems->dir === 'ltr' ? 'selected' : '' }}>English</option>
                    </select>
                </div>

                <hr>

                <div class="form" >
                    <label class="label">السطر الأول للسؤال:</label><br>
                    <textarea name="qst_1st_line" placeholder="نص السؤال ..." minlength="7" class="title">{{ $ExamItems->qst_1st_line }}</textarea>
                </div>

                <div class="form" >
                    <label class="label"> السطر الثاني للسؤال :</label><br>
                    <textarea name="qsts" placeholder="نص السؤال ..." minlength="7" class="title">{{ $ExamItems->qsts }}</textarea>
                </div>

                <hr>

                <div class="form" >
                    <label class="label"> شكل السؤال :</label>
                    <select class="input the_type" name="the_type">
                        <option value="" disabled selected>اختر الشكل</option>
                        <option  value="radio" {{ $ExamItems->the_type === 'radio' ? 'selected' : '' }}>معه اختيارات ويمكن اختيار واحد فقط</option>
                        <option value="checkbox" {{ $ExamItems->the_type === 'checkbox' ? 'selected' : '' }}>معه اختيارات ويمكن اختيار واحد أو أكثر</option>
                        <option  value="text" {{ $ExamItems->the_type === 'text' ? 'selected' : '' }}>الإجابة عليه ستكون قصيرة</option>
                        <option value="textarea" {{ $ExamItems->the_type === 'textarea' ? 'selected' : '' }}>الإجابة عليه ستكون طويلة</option>
                    </select>
                </div>

                <hr>

                <div class="form answerField">
                    <label class="label"> الجواب الصحيح :</label><br>
                    <textarea name="correct_answer" placeholder="أكتب الإجابة الصحيحة هنا ...">{{ $ExamItems->correct_answer }}</textarea>
                </div>

                <p class="for_radio">باقي الاختيارات خاطئة :</p>

                @php
                    $choice1Array = $ExamItems->choice1 ? explode(',', $ExamItems->choice1) : [];
                    $choice2Array = $ExamItems->choice2 ? explode(',', $ExamItems->choice2) : [];
                    $choice3Array = $ExamItems->choice3 ? explode(',', $ExamItems->choice3) : [];
                @endphp
            
            <div class="form choiceFields">
                <div>
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الأول:</label>
                    <input 
                        class="input choicetext" 
                        type="text" 
                        name="choice1[]" 
                        placeholder="أدخل النص هنا..." 
                        value="{{ $choice1Array[0] ?? '' }}">
                    <select class="small-input key choiceKey" name="choice1[]">
                        <option value="" disabled {{ empty($choice1Array[1]) ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option class="wrong" value="false" {{ isset($choice1Array[1]) && $choice1Array[1] === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option class="correct" value="true" {{ isset($choice1Array[1]) && $choice1Array[1] === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                </div>

                <hr>

                <div>
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الثاني:</label>
                    <input 
                        class="input choicetext" 
                        type="text" 
                        name="choice2[]" 
                        placeholder="أدخل النص هنا..." 
                        value="{{ $choice2Array[0] ?? '' }}">
                    <select class="small-input key choiceKey" name="choice2[]">
                        <option value="" disabled {{ empty($choice2Array[1]) ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option class="wrong" value="false" {{ isset($choice2Array[1]) && $choice2Array[1] === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option class="correct" value="true" {{ isset($choice2Array[1]) && $choice2Array[1] === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                </div>

                <hr>

                <div>
                    <label class="label"><i class="fas fa-dot-circle"></i> الاختيار الثالث:</label>
                    <input 
                        class="input choicetext" 
                        type="text" 
                        name="choice3[]" 
                        placeholder="أدخل النص هنا..." 
                        value="{{ $choice3Array[0] ?? '' }}">
                    <select class="small-input key choiceKey" name="choice3[]">
                        <option value="" disabled {{ empty($choice3Array[1]) ? 'selected' : '' }}>صحيح أم خطأ؟</option>
                        <option class="wrong" value="false" {{ isset($choice3Array[1]) && $choice3Array[1] === 'false' ? 'selected' : '' }}>خطأ</option>
                        <option  class="correct" value="true" {{ isset($choice3Array[1]) && $choice3Array[1] === 'true' ? 'selected' : '' }}>صحيح</option>
                    </select>
                </div>
            </div>

                <hr>

                
                <div>
                    <label class="label"> صورة تظهر أسفل السؤال:</label>
                    <input type="file" name="qst_img" onchange="previewImage(this, 'qst_img_preview')">
                    @if ($ExamItems->qst_img)
                        <div class="preview">
                            <img    src="{{ $ExamItems->qst_img ? 
                                            asset('images/exams/' . $ExamItems->qst_img) 
                                            : asset('default-image.jpg') }}" 
                                    alt="صورة السؤال" id="qst_img_preview" class="img-preview">

                        </div>
                    @endif
                </div>

                <hr>

                <div>
                    <label class="label"> رسالة تظهر عندما تكون الإجابة صحيحة:</label><br>
                    <textarea name="if_choising_correct" placeholder="أكتب رسالة تظهر عندما تكون الإجابة صحيحة ...">{{ $ExamItems->if_choising_correct }}</textarea>

                    <label class="label"> صورة تظهر إذا كانت الإجابة صحيحة:</label>
                    <input type="file" name="img_if_right_answer" onchange="previewImage(this, 'right_answer_preview')">
                    @if ($ExamItems->img_if_right_answer)
                        <div class="preview">
                            <img src="{{ asset('images/exams/' . $ExamItems->img_if_right_answer) }}" alt="صورة الإجابة الصحيحة" id="right_answer_preview" class="img-preview">
                        </div>
                    @endif
                </div>

                <hr>

                <div class="form" >
                    <label class="label"> رسالة تظهر إذا كانت الإجابة خاطئة:</label><br>
                    <textarea name="if_its_wrong_answer" placeholder="أكتب رسالة تظهر إذا كانت الإجابة خاطئة ...">{{ $ExamItems->if_its_wrong_answer }}</textarea>

                    <label class="label"> صورة تظهر إذا كانت الإجابة خاطئة:</label>
                    <input type="file" name="img_if_wrong_answer" onchange="previewImage(this, 'wrong_answer_preview')">
                    @if ($ExamItems->img_if_wrong_answer)
                        <div class="preview">
                            <img src="{{ asset('images/exams/' . $ExamItems->img_if_wrong_answer) }}" alt="صورة الإجابة الخاطئة" id="wrong_answer_preview" class="img-preview">
                        </div>
                    @endif
                </div>

                <hr>

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
        </script>

    </x-layoutAdm>
    