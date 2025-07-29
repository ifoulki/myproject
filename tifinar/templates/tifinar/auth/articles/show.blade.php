<x-layoutAdm>
    
    <div class="content">
        <h1> @section('title')
                {{ $article->title }}
            @show
        </h1>

        @php
            $images = explode(',', $article->Myimage);
            $images = array_reverse($images)
        @endphp

        <figure class="flex-100">
            <img src="{{ asset('images/articles/' . $images[0]) }}" alt="{{ $article->title }}">
        </figure>

        <div class="Author">
            {{ $article->Author }}
        </div>

        <div class="date"> تاريخ النشر:
            {!! $article->updated_at !!}
        </div>
        @php
            $direction = $article->dir;
        @endphp
        <div <?= isset($direction) ? "dir=$direction" : '' ?>>
            {!! $article->Mysubject !!}
        </div>
        @php
            $autres = explode(',', $article->autre);
            $autres = array_reverse($autres)
        @endphp
            <img src="{{ asset('images/articles/' . $autres[0] ) }}" alt="الصورة : {{ $article->title }}">


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
            
            <form action="{{ route('articles.destroy', $article) }}" method="POST" style="margin: 0;">
                @csrf
                @method('DELETE')
                <button class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> 
                    حدف المقال
                </button>
            </form>

            <div style="display: flex; gap: 15px; align-items: center;">
                <a href="{{ route('articles.edit', $article) }}" class="btn btn-primary">
                    <i class="fas fa-edit"></i> تعديل المقال
                </a>
            </div>
            
        
        </div>
        
        <hr>

        </section>
        <hr>
</x-layoutAdm>
