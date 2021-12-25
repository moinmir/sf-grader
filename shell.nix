{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
  snapfaas = import (fetchFromGitHub {
    owner = "princeton-sns";
    repo = "snapfaas";
    rev = "1d634cb66d69c4c5eed741d19ff6ff202dbd66fa";
    sha256 = "1vrmm5nmydyhf3xbri9mpl9kpcd4ybb1waaynkx99l1hz9md4rg4";
  }) { inherit pkgs; release = false; };
in mkShell {
  buildInputs = [ lkl snapfaas ];
  shellHook = ''
    # Mark variables which are modified or created for export.
    set -a
    source ${toString ./.env}
    set +a
  '';
}
