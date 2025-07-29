<x-layoutAdm>
    <article class="content">
        <h1> @section('title')
                {{ $video->title }}
            @show
        </h1>

        @php
            $images = explode(',', $video->Myimage);
        @endphp

        <div class="Author">
            {{ $video->Author }}
        </div>

        <div class="date"> تاريخ النشر:
            {{ $video->updated_at }}
        </div>
        @php
            $direction = $video->dir;
            $originalLink = $video->Mysubject;
            $isYouTube = preg_match('/^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)/', $originalLink);
            $isMp4 = preg_match('/\.mp4$/i', $originalLink);
        @endphp
        
        @if (isset($originalLink))
            <div {{ isset($direction) ? "dir=".$direction : '' }} style="position: relative; padding-bottom: 56.25%;" >

                @if ($isYouTube)
                    <iframe 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                        src="{{ $originalLink }}" 
                        title="YouTube video player" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowfullscreen
                    ></iframe>
                @elseif ($isMp4)
                        <video controls style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                            <source src="{{ asset('videos_mp4/' . $originalLink) }}" type="video/mp4">
                            متصفحك لا يدعم تشغيل الفيديو.
                        </video>
                @endif
            </div>
        @endif

        {{ $video->autre }}

        <br>
        <?php
            $filename = Request::path();
            $path_parts = basename($filename);
        ?>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="#" onclick="history.back(); return false;" class="btn btn-secondary">
                <i class="fas fa-arrow-right"></i>
                العودة للصفحة السابقة
            </a>
            
            <form action="{{ route('auth.videos.destroy', $video) }}" method="POST" style="margin: 0;">
                @csrf
                @method('DELETE')
                <button class="btn btn-danger">
                    <i class="fas fa-trash-alt"></i> 
                    حدف الفيديو
                </button>
            </form>

            <div style="display: flex; gap: 15px; align-items: center;">
                    <a href="{{ route('auth.videos.edit', $video) }}" class="btn btn-primary">
                    <i class="fas fa-edit"></i> تعديل الفيديو
                </a>
            </div>

        </div>

        <hr>

        @include('auth.videos.edditComments')

    </article>
</x-layoutAdm>
