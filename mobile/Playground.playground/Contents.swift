import SwiftUI
import Alamofire

// https://stackoverflow.com/questions/26364914/http-request-in-swift-with-post-method
// https://developer.apple.com/documentation/foundation/url_loading_system/uploading_data_to_a_website




//let url = URL(string: "http://127.0.0.1:5000/send-data")!
//var components = URLComponents(url: url, resolvingAgainstBaseURL: false)!
//
//components.queryItems = [
//    URLQueryItem(name: "patient_id", value: "12345"),
//    URLQueryItem(name: "timestamp", value: "2019-04-09"),
//    URLQueryItem(name: "data", value: "1,2,3\n4,5,6")
//]
//
//let query = components.url!.query
//print(String(query!))

let data = Data("data".utf8)
AF.upload(data, to: "https://httpbin.org/post").responseDecodable(of: HTTPBinResponse.self) { response in
    debugPrint(response)
}



// ####################################################################################





//struct Payload: Codable {
//    let patient_id: String
//    let timestamp: String
//    let data: String
//}
//
//// ...
//
//let p = Payload(patient_id: "12345",
//                timestamp: "2019-04-09",
//                data: "a,b,c\nx,y,z")
//let uploadData = try JSONEncoder().encode(p)
//
//let url = URL(string: "http://127.0.0.1:5000/send-data")!
//var request = URLRequest(url: url)
//request.httpMethod = "POST"
//request.setValue("application/json", forHTTPHeaderField: "Content-Type")
//
//
//let task = URLSession.shared.uploadTask(with: request, from: uploadData) { data, response, error in
//    if let error = error {
//        print("error: \(error)")
//        return
//    }
//    guard let response = response as? HTTPURLResponse,
//        (200...299).contains(response.statusCode) else {
//        print("server error")
//        return
//    }
//    if
//        let data = data,
//        let dataString = String(data: data, encoding: .utf8) {
//        print("got data: \(dataString)")
//    }
//}
//task.resume()

