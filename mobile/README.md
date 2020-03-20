# Sparkle WatchOS and iOS applications

* project directory

```
.
├── README.md
├── mobile                             # iOS files
├── mobile\ WatchKit\ App              # watchOS UI files
├── mobile\ WatchKit\ Extension        # watchOS backend/swift logic
└── mobile.xcodeproj
```

* Notes:
    - UI needs refactoring
    - consider using only a single screen and dedicating efforts to data transfer functionality
    - Need to flesh out how to access send and send it out.

### Current functionality

Used [gifify](https://github.com/vvo/gifify) to generate gif from command line. Specifically, 

```
gifify apps.mov -o apps.gif --colors 255
```

![current functionality](apps.gif)
