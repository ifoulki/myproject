<x-layoutAdm>

    <div class="content">
        <h1> @section('title')
                {{ $exam->title }}
            @show
        </h1>

        @php
            $images = explode(',', $exam->Myimage);
        @endphp

        <figure class="flex-100">
            <img src="{{ asset('images/exams/' . $images[0]) }}" alt="{{ $exam->title }}">
        </figure>

        <div class="Author">
            {{ $exam->Author }}
        </div>

        <div class="date"> تاريخ النشر:
            {!! $exam->date !!}
        </div>
        @php
            $direction = $exam->dir;
        @endphp
        <div <?= isset($direction) ? "dir=$direction" : '' ?>>
            {!! $exam->Mysubject !!}
        </div>

        {{ $exam->autre }}

        <br>
        <?php
        $filename = Request::path();
        $path_parts = basename($filename); 
        ?>

        <br>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="#" onclick="history.back(); return false;" class="btn btn-secondary">
                <i class="fas fa-arrow-right"></i>
                العودة للصفحة السابقة
            </a>
            
            <form action="{{ route('exams.destroy', $exam) }}" method="POST" style="margin: 0;">
                @csrf
                @method('DELETE')
                <button class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> 
                    حدف الاختبار
                </button>
            </form>

            <div style="display: flex; gap: 15px; align-items: center;">
                <form action="{{ route('exams.update', $exam) }}" method="POST" style="margin: 0;">
                    @csrf
                    @method('PATCH')
                    
                    <button title="{{ $exam->visibility_status == 'public' ? 'أنقر لجعله يظهر للمدراء فقط' : 'أنقر لجعله يظهر للجميع ' }}" class="btn {{ $exam->visibility_status == 'public' ?  'btn-success':'btn-warning'  }}" type="submit" name="visibility" value="{{ $exam->visibility_status == 'public' ? 'restricted' : 'public' }}">
                        <i class="fas {{ $exam->visibility_status == 'public' ?  'fa-eye':'fa-eye-slash'  }}"></i>
                        {{ $exam->visibility_status == 'public' ? 'الاختبار يظهر للجميع' : 'الاختبار يظهر للمدراء فقط ' }}
                    </button>
                </form>
            
                <a href="{{ route('exams.edit', $exam) }}" class="btn btn-primary">
                    <i class="fas fa-edit"></i> تعديل الاختبار
                </a>

            </div>

        </div>

        <hr>

        <h2>إضافة تعليق :</h2>

        <form method="post">
            <label class="label">الإسم الكامل :</label><br>
            <input class="input" type="text" name="name" placeholder="الإسم الكامل"><br>
            <hr>
            <label class="label">البريد الإلكتروني : </label><br>
            <input class="input" type="text" name="email" placeholder="البريد الإلكتروني"><br>
            <hr>
            <label class="label">نص التعليق :</label><br>
            <textarea name="comment" placeholder="نص التعليق"></textarea>
            <input type="submit" class="add_btn" name="send_cmt" value="نشر التعليق">
        </form>
        <hr>
        {{-- @include('layout.sidebar') --}}
        </section>
        <hr>
</x-layoutAdm>
