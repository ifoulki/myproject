<x-layoutAdm page="لائحة الأعضاء">

    <article class="content">
        @php
            $roles = [
                'user' => 'لائحة مستخدمي الموقع',
                'admin' => 'لائحة مسؤولي الموقع',
                'content_creator' => 'لائحة منشئي المحتوى',
            ];
            $title = $roles[request('role')] ?? 'لائحة الأعضاء';
        @endphp
    
    <h1>{{ $title }}</h1>

        <div class="filter mt-4 p-4 border rounded shadow-sm bg-light">
            <form method="GET" action="{{ route('users.index') }}" class="d-flex flex-column flex-md-row align-items-md-center mb-3">
                <div class="input-group border rounded flex-grow-1 d-flex">
                    <input type="text" class="form-control search-input border-0 flex-grow-1" id="search" name="search" placeholder="ابحث عن عضو" value="{{ request('search') }}">
                    <button type="submit" class="btn btn-outline-primary search-btn flex-shrink-0" style="width: 50px;">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>

        </div>

        @if ($users->isEmpty())
            <p>لا توجد بيانات للعرض.</p>
        @else

            <div class="container mt-5">

                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="thead-dark">
                            <tr>
                                <th class="img-contacnt">ID</th>
                                <th class="img-contacnt">الصورة</th>
                                <th>الاسم</th>
                                <th>Tel</th>
                                <th>التحكم</th>
                            </tr>
                        </thead>
                        <tbody>
                            @php
                                $currentUserId = Auth::user()->id;
                                $currentUser = Auth::user();

                            @endphp
                            @foreach ($users as $User)

                            @if ($User->id != $currentUserId)
                                @php
                                    $path = explode(',', $User->path);
                                    shuffle($path);
                                    if (count($path) > 0 && !empty($path[0] )) {
                                        $src = asset( $path[0]);
                                    } else {
                                        $src = $User->gender == 'Female' ? asset('assets/female.webp') : asset('assets/male.webp');
                                    }
                                @endphp
                                <tr>
                                    <td><a href="{{ route('auth.users.show', $User) }}">{{ $User->id }}</a></td>
                                    <td class="img-contacnt">
                                        <a href="{{ $src }}" data-lightbox="gallery" data-title="{{ $User->Prenom }} {{ $User->Nom }}">
                                            <img src="{{ $src }}" alt="{{ $User->Prenom }} {{ $User->Nom }}" class="img-thumbnail" style="width: 80px; height: 80px;">
                                        </a>
                                    </td>
                                    <td>
                                        <a href="{{ route('auth.users.show', $User) }}">
                                            {{ $User->Prenom }} {{ $User->Nom }}
                                        </a>
                                    </td>
                                    <td>
                                        <a href="{{ route('auth.users.show', $User) }}">
                                            {{ $User->Tel }}
                                        </a>
                                    </td>
                                    <td>
                                        <div class="friendship-section">

                                            @php
                                                $friendsArray = explode(',', $currentUser->friends);
                                                $is_friend = (in_array($User->id, $friendsArray)) ? true: false;

                                                $UserFriendRequests = explode(',', $User->friend_requests);
                                                $FriendRequestSent = (in_array($currentUser->id, $UserFriendRequests)) ? true : false;

                                                $FriendRequestsArray = explode(',', $currentUser->friend_requests);
                                                $FriendRequest = (in_array($User->id, $FriendRequestsArray)) ? true : false;

                                            @endphp
                                            
                                            <div>                                                       
                                                @if ($FriendRequestSent)
                                                    <form action="{{ route('cancelFriendRequest', ['userId' => $User->id]) }}" method="POST">
                                                        @csrf
                                                        <button type="submit" class="btn btn-warning">إلغاء طلب صداقة</button>
                                                    </form>
                                                @elseif($FriendRequest)
                                                    <form action="{{ route('acceptFriendRequest', ['userId' => $User->id]) }}" method="POST">
                                                        @csrf
                                                        <button type="submit" class="btn btn-success">قبول طلب صداقة</button>
                                                    </form>
                                                    <form action="{{ route('rejectFriendRequest', ['userId' => $User->id]) }}" method="POST">
                                                        @csrf
                                                        <button type="submit" class="btn btn-danger">رفض طلب صداقة</button>
                                                    </form>
                                                @elseif ( $is_friend )
                                                    <form action="{{ route('removeFriend', ['userId' => $User->id]) }}" method="POST">
                                                        @csrf
                                                        <button type="submit" title="صديق بالفعل .. هل تريد إزالته كصديق؟" class="btn btn-secondary" >
                                                            <i class="fa fa-user-check" aria-hidden="true"></i> صديق
                                                        </button>
                                                    </form>
                                                @else 
                                                    <form action="{{ route('sendFriendRequest', $User->id) }}" method="POST">
                                                        @csrf
                                                        <button type="submit" class="btn btn-primary">إرسال طلب صداقة</button>
                                                    </form>
                                                    @endif
                                                        <button onclick="redirectToForm( {{$User->id}})" class="send-button">
                                                            <i class="fas fa-comment"></i> إرسال رسالة
                                                        </button>
                                            </div>
                                        </div>
                                        
                                    </td>
                                </tr>
                                @endif
                            @endforeach
                        </tbody>
                    </table>
                    
                </div>
            </div>
        @endif

        <div class="pagination-wrapper">
            {{ $users->appends(request()->input())->links('vendor.pagination.bootstrap-5') }}
        </div>
    </article>    


<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lightbox2/dist/js/lightbox-plus-jquery.js"></script>      

<script>
function redirectToForm(userId) {
    const url = `/%D8%A7%D8%AA%D8%B5%D9%84_%D8%A8%D9%86%D8%A7?user_id=${userId}`;
    window.location.href = url;
}
</script>

</x-layoutAdm>