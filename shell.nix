{
  pkgs ? import <nixpkgs> {},
  snapfaasSha256 ? "19c6r7h7zrww3n9wjyznzjhq4avjyixzc846mvavr5x7nqwa1qva",
  snapfaasRev ? "8c84242b6b682f9b3bd0cb2a075a7a8c3dbfb81d",
  snapfaasSrc ? pkgs.fetchFromGitHub {
    owner = "princeton-sns";
    repo = "snapfaas";
    rev = snapfaasRev;
    sha256 = snapfaasSha256;
  },
  release ? false
}:

with pkgs;
let
  snapfaas = import snapfaasSrc { inherit pkgs release; };
in mkShell {
  buildInputs = [ lkl snapfaas ];
  shellHook = ''
    # Mark variables which are modified or created for export.
    set -a
    source ${toString ./.env}
    set +a
  '';
}
