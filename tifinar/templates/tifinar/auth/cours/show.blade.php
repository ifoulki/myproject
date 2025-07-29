<x-layoutAdm>

    <div class="content">
        <h1> @section('title')
                {{ $cour->title }}
            @show
        </h1>

        @php
            $images = explode(',', $cour->Myimage);
        @endphp

        <figure class="flex-100">
            <img src="{{ asset('images/cours/' . $images[0]) }}" alt="{{ $cour->title }}">
        </figure>

        <div class="Author">
            {{ $cour->Author }}
        </div>

        <div class="date"> تاريخ النشر:
            {!! $cour->date !!}
        </div>
        @php
            $direction = $cour->dir;
        @endphp
        <div <?= isset($direction) ? "dir=$direction" : '' ?>>
            {!! $cour->Mysubject !!}
        </div>

        {{ $cour->autre }}

        @php
            $filename = Request::path();
            $path_parts = basename($filename);
        @endphp

        <br>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="#" onclick="history.back(); return false;" class="btn btn-secondary">
                <i class="fas fa-arrow-right"></i>
                العودة للصفحة السابقة
            </a>
            
            <form action="{{ route('cours.destroy', $cour) }}" method="POST" style="margin: 0;">
                @csrf
                @method('DELETE')
                <button class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> 
                    حدف الدرس
                </button>
            </form>

            <div style="display: flex; gap: 15px; align-items: center;">
                <form action="{{ route('cours.update', $cour) }}" method="POST" style="margin: 0;">
                    @csrf
                    @method('PATCH')
                    
                    <button title="{{ $cour->visibility_status == 'public' ? 'أنقر لجعله يظهر للمدراء فقط' : 'أنقر لجعله يظهر للجميع ' }}" class="btn {{ $cour->visibility_status == 'public' ?  'btn-success':'btn-warning'  }}" type="submit" name="visibility" value="{{ $cour->visibility_status == 'public' ? 'restricted' : 'public' }}">
                        <i class="fas {{ $cour->visibility_status == 'public' ?  'fa-eye':'fa-eye-slash'  }}"></i>
                        {{ $cour->visibility_status == 'public' ? 'الدرس يظهر للجميع' : 'الدرس يظهر للمدراء فقط ' }}
                    </button>
                </form>
            
                <a href="{{ route('cours.edit', $cour) }}" class="btn btn-primary">
                    <i class="fas fa-edit"></i> تعديل الدرس
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
