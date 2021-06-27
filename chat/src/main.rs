use tokio::{io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader}, net::TcpListener, sync::broadcast};

#[tokio::main] 
async fn main() {
    let listener = TcpListener::bind("localhost:8080").await.unwrap();

    let (tx, mut _rx) = broadcast::channel::<(String, std::net::SocketAddr)>(10);


    loop {
    let (mut socket, addr) = listener.accept().await.unwrap();
    let tx = tx.clone();
    let mut rx = tx.subscribe();
    tokio::spawn(async move {

        let (read, mut writer) = socket.split();
        let mut reader = BufReader::new(read);
        let mut line = String::new();
    
        loop {
            // select is useful when concurrent things work on a shared state and there is a fininte number of things
            tokio::select! {  
                result = reader.read_line(&mut line) => {
                    if result.unwrap() == 0 {
                        break;
                    }
                    tx.send((line.clone(), addr)).unwrap();
                    line.clear();
                }
                result = rx.recv() => {
                    let (msg, other_addr) = result.unwrap();

                    if addr != other_addr {
                    writer.write_all(msg.as_bytes()).await.unwrap();
                    }
                    }
                }
            }
        });
    }
}