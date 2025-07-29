<x-layoutAdm>

    <div class="content">
        <h1> @section('title')
                {{ $book->title }}
            @show
        </h1>

        <figure class="flex-100">
            <img src="{{ asset( 'images/books/'.$book->Myimage) }}" alt="{{ $book->title }}">
        </figure>

        <div class="Author">
            {{ $book->Author }}
        </div>

        <div class="date"> تاريخ النشر:
            {!! $book->date !!}
        </div>
        @php
            $direction = $book->dir;
        @endphp
        <div <?= isset($direction) ? "dir=$direction" : '' ?>>
            {!! $book->Mysubject !!}
        </div>

        رابط تحميل كتاب :
        <script>
            function convertSpacesToUnderscores(url) {
                return url.replace(/\s+/g, '_');
            }

            let originalText = "{{ $book->autre }}";
            let urlText = convertSpacesToUnderscores(originalText);

            document.addEventListener("DOMContentLoaded", function() {
                document.getElementById("dynamic-link").href = "{{ asset('ebookZone') }}/" + urlText;
            });
        </script>

        <a id="dynamic-link" target="blank"> {{ $book->title }} </a>

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
            
            <form action="{{ route('books.destroy', $book) }}" method="POST" style="margin: 0;">
                @csrf
                @method('DELETE')
                <button class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> 
                    حدف الكتاب
                </button>
            </form>

            <div style="display: flex; gap: 15px; align-items: center;">
                <form action="{{ route('books.update', $book) }}" method="POST" style="margin: 0;">
                    @csrf
                    @method('PATCH')
                    
                    <button title="{{ $book->visibility_status == 'public' ? 'أنقر لجعله يظهر للمدراء فقط' : 'أنقر لجعله يظهر للجميع ' }}" class="btn {{ $book->visibility_status == 'public' ?  'btn-success':'btn-warning'  }}" type="submit" name="visibility" value="{{ $book->visibility_status == 'public' ? 'restricted' : 'public' }}">
                        <i class="fas {{ $book->visibility_status == 'public' ?  'fa-eye':'fa-eye-slash'  }}"></i>
                        {{ $book->visibility_status == 'public' ? 'الكتاب يظهر للجميع' : 'الكتاب يظهر للمدراء فقط ' }}
                    </button>
                </form>
            
                <a href="{{ route('books.edit', $book) }}" class="btn btn-primary">
                    <i class="fas fa-edit"></i> تعديل الكتاب
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
