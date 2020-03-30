import SwiftUI

// struct to display list of messages sent to s3
struct Message: Identifiable {
    var id = UUID()
    var dateString: String
}
var messagesReceived: [Message] = []
messagesReceived.append(Message(dateString: "2020"))
print(messagesReceived)
