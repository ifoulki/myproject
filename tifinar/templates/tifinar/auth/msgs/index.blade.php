<x-layoutAdm :page="'✉️ قراءة الرسائل'">
        <article class="content">
            <h1 class="big-title" id="title">قراءة الرسائل</h1>

            @if ($msgs->count())
                @foreach ($msgs as $msg)
                @php
                    $authorId=$msg->author_id;
                @endphp 
                    <div class="form">
                        <div class="listes-contenu-art" dir="{{ $msg->dir }}">
                            <div class="msg-status">
                                @if ($msg->Author == Auth::user()->Prenom.' '.Auth::user()->Nom)
                                    <i class="fas fa-paper-plane" style="color: #1cd20b; font-size: 1.2em;"></i>
                                    <span style="color: rgb(210, 141, 11);">{{ $msg->dir == 'rtl' ? 'رسالة مرسلة' : 'Sent Message' }}</span>

                                @elseif ($msg->status == 'read')
                                    <i class="fas fa-envelope-open-text" style="color: orange;"></i>
                                    <span style="color: orange;">{{ $msg->dir == 'rtl' ? 'مقروءة' : 'Read' }}</span>
                                @elseif ($msg->status == 'unread')
                                    <i class="fas fa-envelope" style="color: #1cd20b;"></i>
                                    <span style="color: #1cd20b;">{{ $msg->dir == 'rtl' ? 'رسالة واردة جديدة' : 'New Incoming Message' }}</span>
                                @elseif ($msg->status == 'important')
                                    <i class="fas fa-envelope-open-text" style="color: #1cd20b; font-size: 1.2em;"></i>
                                    <span style="color: rgb(210, 141, 11);">{{ $msg->dir == 'rtl' ? 'رسالة مهمة' : 'Important Message' }}</span>
                                    <i class="fas fa-exclamation-circle" style="color: #1cd20b; font-size: 0.8em; position: relative; top: -5px;"></i>
                                @else
                                    <i class="fas fa-envelope" style="color: grey;"></i>
                                    <span style="color: grey;">{{ $msg->dir == 'rtl' ? 'رسالة ' : 'Message' }}</span>
                                @endif

                            </div>

                            <a href="{{ route('msgs.show', $msg) }}">
                                <div class="text-center d-flex justify-content-start align-items-center bg-light" style="padding: 10px;">
                                    @php
                                        $images = explode(',', $msg->author_img);
                                    @endphp
                                    <!-- حاوية الصورة -->
                                    <figure class="m-0" style="width: 10%; text-align: center;">
                                        <img style="width: 100%; border-radius: 50%; border: solid 2px #007bff;"
                                             src="{{ asset($images[0] ?? 'default-image.png') }}"
                                             alt="{{ $msg->Author }}"
                                             class="img-fluid">
                                        <figcaption class="text-muted mt-2"> {{ $msg->Author }}</figcaption>
                                    </figure>
                            
                                    <!-- الخط العمودي -->
                                    <div style="border-left: 2px solid #007bff; height: 80%; margin: 0 15px;"></div>
                            
                                    <!-- النص -->
                                    <p style="color: black; text-align: justify; margin: 0;">
                                        @if ($msg->title !="standard")
                                        <h2 class="label">{!!$msg->title!!}</h2>
                                        @else
                                            {!! Str::limit($msg->Mysubject, 100) !!}
                                        @endif
                                    </p>
                                </div>
                            </a>
                            

                            <div class="btn-container">

                                <a href="{{ route('msgs.show', $msg) }}" class="btn btn-success">
                                    <i class="fas fa-envelope-open-text"></i> فتح الرسالة
                                </a>

                                <button onclick="redirectToForm({{ $authorId }})" class="btn btn-primary">
                                    <i class="fas fa-reply"></i> رد
                                </button>

                                <form action="{{ route('msgs.destroy', $msg) }}" method="POST" style="margin: 0;">
                                    @csrf
                                    @method('DELETE')
                                    <button class="btn btn-danger">
                                        <i class="fas fa-trash-alt"></i> حذف الرسالة
                                    </button>
                                </form>

                            </div>
                        </div>
                    </div>
                @endforeach

                <div class="pagination-wrapper">
                    {{ $msgs->links('vendor.pagination.bootstrap-5') }}
                </div>
            @else
                <p>ليس لديك أية رسائل واردة</p>
            @endif
        </article>
        <script>
            function redirectToForm(authorId) {
                const url = `/%D8%A7%D8%AA%D8%B5%D9%84_%D8%A8%D9%86%D8%A7?user_id=${authorId}`;
                window.location.href = url;
            }
        </script>
        
</x-layoutAdm>
