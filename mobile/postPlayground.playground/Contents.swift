import Alamofire

func getTimestamp() -> String {
    let now = Date()
    let formatter = DateFormatter()
    formatter.timeZone = TimeZone.current
    formatter.dateFormat = "yyyy-MM-dd_HH:mm:ss"
    let dateString = formatter.string(from: now)
    return dateString
}
// exmaple HTTP parameters:
let parameters: [String: String] = [
    "patient_id": "1"
    ]

struct rxMetadata: Decodable {
    let timestamp: String
    let drug: String
    let desc: String
    let amount: Int
}



func sendPost(parameters: [String: String], _ completion: @escaping ([rxMetadata]?) -> Void){
    AF.request("http://127.0.0.1:5000/mobile-login",
               method: .post,
               parameters: parameters,
               encoder: JSONParameterEncoder.default).responseDecodable(of: [rxMetadata].self) { response in
//                    debugPrint(response)
                guard let schedule = response.value else { return }
                completion(schedule)
    }
}
sendPost(parameters: parameters) { schedule in
    guard let schedule = schedule else { return }
    print("schedule: \(schedule)")
}
