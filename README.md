# xargswin
Minimalist Xargs for Windows

Minimalist Xargs for Windows, currently following options
are implemented:

# Arguments
    -I              replace_str
    -t, --verbose   Verbose mode

# Example Usage
    * Create str(s) to operate on and write to a file
        echo hi> test.txt
        echo there>>test.txt
        echo how?>>test.txt
        
    * Pipe the contents of the text file to the file to execute:
        type test.txt | xargswin.exe -I{} "echo {}"

    * Alternatively, query string does not need to be specified:
        type test.txt | xargswin.exe echo {}

