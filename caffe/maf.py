#!/usr/bin/env python
# coding: ISO8859-1
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
maf - a waf extension for automation of parameterized computational experiments
"""

# NOTE: coding ISO8859-1 is necessary for attaching maflib at the end of this
# file.

import os
import os.path
import shutil
import subprocess
import sys
import tarfile
import waflib.Context
import waflib.Logs

TAR_NAME = 'maflib.tar'
NEW_LINE = '#XXX'.encode()
CARRIAGE_RETURN = '#YYY'.encode()
ARCHIVE_BEGIN = '#==>\n'.encode()
ARCHIVE_END = '#<==\n'.encode()

class _Cleaner:
    def __init__(self, directory):
        self._cwd = os.getcwd()
        self._directory = directory

    def __enter__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._cwd)
        if exc_type:
            self.clean()
        return False

    def clean(self):
        try:
            path = os.path.join(self._directory, 'maflib')
            shutil.rmtree(path)
        except OSError:
            pass

def _read_archive(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                raise Exception('archive not found')
            if line == ARCHIVE_BEGIN:
                content = f.readline()
                if not content or f.readline() != ARCHIVE_END:
                    raise Exception('corrupt archive')
                break

    return content[1:-1].replace(NEW_LINE, '\n'.encode()).replace(
        CARRIAGE_RETURN, '\r'.encode())

def unpack_maflib(directory):
    with _Cleaner(directory) as c:
        content = _read_archive(__file__)

        os.makedirs(os.path.join(directory, 'maflib'))
        os.chdir(directory)

        bz2_name = TAR_NAME + '.bz2'
        with open(bz2_name, 'wb') as f:
            f.write(content)

        try:
            t = tarfile.open(bz2_name)
        except:
            try:
                os.system('bunzip2 ' + bz2_name)
                t = tarfile.open(TAR_NAME)
            except:
                raise Exception('Cannot extract maflib. Check that python bz2 module or bunzip2 command is available.')

        try:
            t.extractall()
        finally:
            t.close()

        try:
            os.remove(bz2_name)
            os.remove(TAR_NAME)
        except:
            pass

        maflib_path = os.path.abspath(os.getcwd())
        return maflib_path

def test_maflib(directory):
    try:
        os.stat(os.path.join(directory, 'maflib'))
        return os.path.abspath(directory)
    except OSError:
        return None

def find_maflib():
    path = waflib.Context.waf_dir
    if not test_maflib(path):
        unpack_maflib(path)
    return path

find_maflib()
import maflib.core
#==>
#BZh91AY&SY�Dx q����\������������� @H�`m>y�6���o�� ��|z��|<t��x<T�P�������6AH���}�N>�%�2�>����҂��ޚ��n�i��O=�/|��  ���������;���=˻u;'p�*#XXX�;׻:K�A"G��O}�^y;Ͷfw|=]��2��g,���.\���z�챪:�#YYY�lmFZ�۽J��ק6`N�l,Os�qՑ�ug3�������kY�ۦ�=�Ҳ���"���"�{�}�n����E���,ݞ���4Ѐ ��OD�mS��z��SM�O�4#YYYL�M	5= MOT�)�=OMM4�L ��  4 $"&D�OM#YYY4Д�S�ԟ�5�'���d#YYY  ѣ@��"A ������a���LO$=��#YYY=M   $��L�!�`iT�SOQ��H�Ѫy���dڏP���ڃ�MD�h4dȧ꧲�G�i��SA����F� �� @��G�}�/���Ad"���J����]�^��!�/)/%����_���I �e�P$&I��U#XXX�PO��?�?�~����k?U�?��o�?����i��7����C�`6����4b��~J��qc�jz���ժ��c��6R)yH����s(�ӄ�fw�^#YYYA�84԰�	�f�^�O��5DA�6"GY�0A_J�D��d`Mq4u�����2+�1��b{}Y�Y��nO���I�W��kLB��]D�+�F�g��B}�G��`�Q �W����3�yg~�ʥZ�c�#�}�c����]�ݚ�TSAAM�Ǖ���mk_��[f��m�m��6F)��T@�*@� }���N���b�-ӓC�U��*����)�"����Y��ll��e,G|��m>��k�z:^�Pz�9�l�Q#XXX��GKy�0EZ�'�՗����vA/c���x؅�|�߻,Iȼ��2IQ�ˣvD�Y���G���ޖ�\+���+�a�0";A|#ݤ�r���f��:����;Y�6m��d� {��#XXX�{���:̊��m�����CK�8|�2|}��ޡ݄�9:՝3�����O!��?�����}@y5����Rȣ�}6��/:ޫ���\aQM�:9��˛j�2翶��:#YYYl����5�[�i���{3)�!Wl��z��޹y��J|S,J�u�����2��̺�~������ϝ�_kܕ&��c����#\�&�P��.�m�q���S�@����(|�[k_D#YYY/%�?f������L�uI�C�_rLc~n����d��	���)ן#D�)����;3�)�jG�uP����SGY]X�I�M���g�xn#�7񦠛�'�필k�Ld��YdO�]�k�'<}�����i�;{O�~M���p�`��֢��h�gw#YYY5J��?V�"a�--����R�s�ݬ�!^��.S�!�B�%;���Q�X�#�!P�"�l��6hi�G&�̔~��n3=���3?���f'�!hl?���3���qcϒ�C|=�[�>�[mj.!�f�+�����m�k��<{:���c�>�~�TT�  nX� �Q^"xP�0 B#XXX�em�|�G�����{��pk�a�����{&�{��v����dx�����2v�-A��8���=$� Z?ޟʢ�ua��<���Z%�������#XXX-�����Ȥm�X˨d����٭,8��|'������p=��7�z��L*��#YYY�.���Q�9���/����f8E��h�u)���jB��MMɆ�v91��<�y�OV���D]~�Hyi �ő����B�Z�7����#�`��<���o㬦J����8��4u�y#�̍�C�����uh#+a�����n�!J��$l���}}�p�C��b�o���4OaJ$����3��}c������8�T;=�pXV�p[3T;#���i=�\;��q�mWo�X��H�H�}�=[�\�����_h�)��LϬ~S���}���ݯ�06ZN<v�#YYY���5��la����o���se���8�ca���nG�� E����O#YYY��r%. rP'��S_\�\6������j:������6������1�q�yU�ۯ*�5v��t\|������+��� ۘ��|6L:2��H'k��9rq�Q��a�si�v��!��M�<r��w��_l�Ie��×Y�k5V9j�&�)�ш��5���f7汑�9�ȱ�-M�_#YYY�8��#����L���!}��/���c4rtS쑠#YYY�[��a? 4W����|̩�u)�q�A�(�k�^��8ߞnh��=Nh#�^�L�$#YYYSm���g��Y��U96m��U�}��*(B؀8#�F�>�.7:�&���F:�AN���w=#YYY&E������n���0�0s@<�5�U]8���=i� ���b4G`�%��ȑAKJF%�KD���	n��T��5��q\_�`~���t����	"�p�f8���Zb�`�j�0�"�������! )�T,��ä.V��	���sԌh)��i�h���@��R�#YYY�1�m���O�p���o,�L��l�*�"I	�!֦��>�m-;t�������Q�k5l�����"�H$�^�oya�0"g��Z[��DPJP��B���@U*�P&"8���6�*��0�@�~�������4�_������ܿ4�>^�0谌a�Ȫ8Ms���P�{�ڄ-τ�I�@!̥N��w6���Q����F���:z��@9#lx�]4p��-k��*R0~�6����i��e��u�$=��G��:�9��|ȟ�7�#XXX��2�:z'[Dɱ�	��AM'G��8¼�D���\�p���8r8ob� ݒ�;�8��}o�&،<:m!��Grk�;�#YYY��$����m)9p��Bp�J4&�#XXX�s��ڝ�_�%cr�"xz'������sPqr���0|jfnu+I#XXX"Wq���woN �%�W-���tQ��ɴa��Ү0�a�Pe�[���c�jp"	Ė�?��L�+ ���M8�����=��2fG��� �2�~p���h�$9J�\y;���yc&��bFam{C�gp[�"���b#�zJ�OGj��[����H�hvǤe� ����$4q�q����[jo{�iH�H�a��i�a`���FGL.�[���D���Ng'�v>�m $�Z*5���m��g�#YYYV��i0���J�B�C�_h�=.5��'fL�j��x��%�\f%����1(Hx�y�El@�%�O�$]�)���ɷ��(�f�H����' !�sCѧ�%��?2�,�2�¸������]L����*%"��f<�����)Ϗ�R5U�j<��2y��&8^l�u�qd�4��MAp�c3qY���������#YYYT���s�����ܭ,�[��UTM�Wg����MI��LX��{eR��w����4�Ӥ���!�0d�9�RK)M��h!�<�4q1�ͨC+$K��E)��E)��T��ڇP���Tj��P#YYY@��"'(bߙ��#)�G�}[>�=O�;Rӂ���f"�V0D�y�@�!]h2�9���5��eze�XA�C\���߾7�,����F����D��';˖��)z���&*U@��\�0iVʰIp�avJx���*� @��i�B���OF��e"�E�p�n'hҰq��&�pq;<�4Sb�"Kg�o��FETC�CH��%@�E��l���ޒq���R2쁥6��͉H� VP��e|���/]��B��B��:����Շ�*;A"(!F#YYYW����hP2�'���(�@J^�NA��[�I� }��Ω��+!A����A���-��ZHt1oB դ� ���k>����|#���!̞%s��ɨ���0�@��Xq�m�`��<R�g�I�1���߮��?��K.�7n��Fg���n�`#YYY7=Tu%�w*�]�C���P��j����j�#YYY���T�Q}�`^��w��I`N�{���`G�1��!�?M�p#XXXṭ2�x;����"Ѳ�O�l�t������B$b��E��X���+�u�z�`F��lџ3vڤEk�#(����LW/n0B����%�(�y���F�B�#YYY�j��%ɐq,#XXX*j�Ӛ1$zJ�Y5�tANs�ٲ��:�H[)�sV+B����UH���9��"cqȍ�n�@�Y���H�f{}z�0ܙ�����{7L}f�nS�Luy�q׈�V�{z4�`@@v0P�C,b���TN+n�����(�(j'|D�-�h��䉯j ��l46��<3�a�u|���24�8pD�i]Q��W#xqL<;��0H\(U."B[�߹��w�H|�v����X=&68����!�d#XXXwY �w�r֋�[{�*�ӣ��b���]CZ���}�-JղPBd�o ��@Y��	d����矊��,�!J�[o�1�H�Aښ�"X�]5�`�RzPe��w0p����e����� w��� q Q�xI��!~�5��iF����f@lە�T=���P`me���Hj�㳠�Uf^,~��[>ڇL�C���h�l�mˇ�&`]V���?jzѮ�Q�#y�3'i@?l��[U���+��?"��M��_�//�6���˅�\9l�+�@�H�Y0sB�<&�(8r�������yC�,FC?~�6��<F*��I�;K{��,`�8���G±Sd$Y�%�.����q� ����Km�q]D�Z�B�RK{@�B���F(u ��S;�1l׼0�@�pm)7���b~�z���P_(<��j4=�m�6ʝd��� D����y�����5�B�������z�D�S#��5Z~)1�=��[��Hw'��I'��m�5�Ѭ/�^ѱ�5s@�p+3�����I��� �A�.p'A���>IDW��[�Z(PqV�T�������2�2���!z }!0��'����_����9�]�۳�y�Y��V8��TG��5 U%5:X�����,*f���U���?B���YחR>��q�#�zm����qD������Z[ŹN"U+��j*��m�<}�e��7�v��g��Ҷ7�>���������t"���h�������M��CXz}���@��d�c���{�Y1�;�����Ɖ�����B?H�o��������0�`Z���}?R�Oy.p>����~	��&E�k,���~������ˢ�4��p�eka?]�L~Fa��V/��n?����ƽA�n_���>ݾ�K���i�S�"�Ϥ�8nĐ #XXX�I6߆�Y����Dy^VN��#S������g�A�HA�&�ˍQ����ɿs�=��ϫ��|�t��¨�f��K����m��/������*���!�d^&g�ϧ��g-�ج�*�2�����#YYYD�A5Z�K��8`��D	@7��o�|Nu�;����hh��י�gO��>��>��O�g�V�H�2��o����CK02>yc�q�R\������5�|�#YYY����Ԗ# �ӌQ�:|"�R�#XXXkM���$J�o:r���j��O"t�D9�G�'���1���Ua"�+8�x�m�y#XXXT����/ ��`?=k~�ۢ9�2�]2>n~r)�BoF�ͦ�b��!z����5�i��/{&����*��EָțصqSPF���in�p��:q�}*�2:&@���"�N�G�����"����uZŅ�D;7������'�Y|�ŵMh��it�U&���a4Sj�<c{�K���pP����C�������izB�(Z�g��ݣ�X��QW�6�1�o7���#���k��{��3k�����������.�5.m/v ��S/-��9e8�Ox�!��PYm�p�����S�v��ޱ��Y�^�w8���U��LC�b��'cd�Ҷ�"�|ޗ_����ץ�qW3���׃R5���٭��i���h��fg ��&�̨�s�J�����<��5LQ�n~#YYY#YYY�k!Ͳ@����ā�8���M��sx�/��w��SF㯳����	����U�;6��Zg���G��c��8-�����r��D��^�]�]�;�L�bR�_³Cݲ��Q��e�7s�X�woa	�@��G�uX�Ur!�ꃈx�E�Ȱ�'�}oġ@"�3t�L��T��Iz__��W.�Z��#>34����o��)Eo:�g�D`6�5�4�ŧ(���"��0���Nf����C�W�xr���Ty�K �l6!����%񺠔�-�brd�Ps��u��ϻ��9��#XXXK�GG���°�2��?a�a�� ��S����0����a�s�#XXXM�������4|��=���y���������UUs��rm�N}Z㆝]�t|c�����Ϝ�)����!��!�g�k9r7j4���c��vա�;F�-*��zs^R�L}�DH*�=�R[�DKîEx�cU �}t��E.���D��R�>`x����m�X�5�����`p��P��7� B�1;w3�����a-H	O�é�����N�X���g���{�9-2�w������r*�����t���~����=�[��Ю�������j�Qp��K2�-?���k�1���N�T�웇O�z ����p鷼}@��Y����PyU({�ʴ�]Q=D�{�%��C�)!J�3+GC�>��w|��W��y��cnX�=)Fn0��`CnU�h/%��_���r_��U6��F�9|��+�Ĳ`�M�2��/��b�-@�]Y��]��*�*�|�"ЎS)v˺)�2śl�)���4�� *�[A@� �`R���XB��^���//Z�lc����m��"R���q0��L�k�$����)ɢ�ݯŜ��/�%#�_D)��||c�@����cn�g��|l?i�Z��3mhCc05�)E�6�Ѫ�K�(�($+=OrI�ꔾ4t*l>G��}:�#XXX|��#�&3O��m�ᑳ�]���t6s�xyBY�� b#r3�i���=A��r��^f��Z-��lO���^�#8����!��z ���{AS�ZW�SJ�Y����r�� �#I�'�G������W2D���$\����_��G.`t ���)t�wF�橘�	d���~��.���Au9���^�Ϝ�ױf	#XXX r@f���KN�����~B���+TV%�	���L%�>�z��q���?���o����'/CD��xD��&��g従o�3�^����r�"� g��~T�\_ܰs̵c�����T?EE{���?�D���*Ћ]p���W�b����B��Hm�������&����m��N�_�.�^4��ܿ۸�nJ~'�a�H��ww���(���@'ڀ���ϧE�􋿓�����6He�yCՐ�D�j����f9��&�-�����O����hW����T|q�t�i,��/�����Z�N9!��.<~}^��=��PwE	_��e#YYY�Gb$�)�"f�h.#YYY��f��'�����,�I,�W�\������Z	˗'����D�-�"�P�,}G������DO��Ѽ��2�S*H���>�wl���N�n�^��^s�����@�����҆�x��YT����$)hS��cNiY"].����e]ۏ%�-<c���)�c?綶A��(G�	��s�I��߇7��иu�3���{����=Br���|�4�L��d~�����$5%P���_GF��[���?�AIH�!UHD>`0?�*jQ#YYYKJІ#YYY�1#XXX ް���8��]�@>3q��Z���#YYY������o�1Aj-<.��|8�����^��Q�#YYY����i?����5�J����@�"�S�x�b~C��Ń"�!�R�f<oѷ�A\&���2������HT�� ?�Z�A#YYY�V����tȹ��F�0[l0�����a��g�w���/ٟ�6h)�6���Qȹ����Ԙgy�BB�[�p�+�NSe/��ڹ뮃���+��<K��%�ϐՓ��by�s�S#�>�CƳ�߸�bX���X���mF���=��x�{���>N���X�o��<�J�����:��!�8Vt_Pt�����^�3�\\J���o<�V��f��}Cq<����:�п4r͞����;�1+�p��+#2�Ȇ%�L�E�G�s#XXX�kEt�k>��\�X�q�h�����J��$��^��^�-"C�Q�J�#XXX��5��'A�|�u��W���k,j*8�[�䞪��>SC�а��]6c\�l�o;�p!�����0��ȇat.VL��d2!ar�te������v8⯲������*��g��*��U�A��<���N����K�UhV��_��ĥ��i��U�:��Yʏ~��S�V����I��^��#ܑ��`��co��Q�!x�\�7�LJ�gY�_�10FX���B��?sr�u�ԫT#����5�,<#YYY�q����,A�i�5����}5P�3!��Iڜ�ɽ�*�)�8���6�B�1+��bd�4���������ƕ�X��X�� ��� �*5�Tz�k��#YYY���XUu�T�HAW�02+�.e���3�G�p;)y_��;iݤ��I�Xq�Q]�hd{-C>�Hdj��C#�2,m6{��>|Ą��͇w���#XXXĵ����gA__�"�>�`�����F-��>�e7G5�f }O��f0qK���6-,9_��=��������y���,�Q�"�������&��^��Ż���[64����F��[Qu������IK����R�J�������$�C?��n��K���r�����i�`��0B#J&����d]$������G��6�W�D~�H�U'�#YYYƵ��r�@`�+����D$�-��������qS���a�U8�f�"�&�����Hޮ:�_b9 D�(�;z9����Qâ�$K�w�!�3�#YYY�YtZev�kbo#�m���9�C�$�zu!^��^��r���Z%����."vJ���>������E�@�����4Z�%��#YYY*��h��/1�JA�kq0�nf@�.CeR	��H���4�&j��Q��5#YYY{	R�T��	j�� �#YYY��7�VE� �� ��a�@�|����Q�u`sZm2���v��������Q"�����U�:�F�Ng��Y�L9��Ys���k2�q�?����"{��YE>^#���� $�:ԸA L7� ��^�b��DI$��R��x�cݐ{82� �������{��@���5܇Z ���`�{(���jme[;�J�X�`ha��#YYY"�����ף/E��<R(*c�ئ��a.:��eG"#�T �N�#XXXl9w��`����#YYY(KDp��HP;�C�`��Rna��_#XXX��P��Qx����1�+9D9I6aA꾁��]��F�\�:]`����N�2��l?Q#YYY�RMRF#XXXR:��NHxm���=//������PL�I��H�#��-��(=*H��s#XXX��C�z��1W�*����}*�P��E� �)hHREHu��T�UW`E`�#i+%eI�&�#YYY�q�����n�&^R��Χ��"�D��l/Z�8w���A��$�ڄ#��.�_�G�pc+��I`l�����O��=��}��~�]i�&��E�H��@�a@�,-(b}�D����QAܴUU��5CUUq�yv}eT�_��ŭUP�	8�6ЌE�(���#XXX�:�Z�T��n�烧p��ro\��DJ=�/H���h}?��sQ��.���`���")w�2�</MI�JX��R����H	�JU#XXX����(��l!�x��l���xܑ�� �&c1ZP�����I3A$1��=?1��$��Y�콸�B�m�+���^�k��ϻ���*�XmM���b��XS���<�7\�q(8��^�s�"�#"*�*�����w�d�t@X�xSh�n��UU���Qz�tI�_�9k翜�3��S�8.F�o�hJ��$i�#YYY�8TN5D��bsĴ�pd����	栱����?��ZH��h"@��$dZB�$%h(�~a��"P�E'pA�9���5j�4�Ǥ#YYY��Ω�妄�꜍t��׉G���r����#XXXlN��*T6��88s3Y+�kM�{�g���� �Mr���z�?8y��>��q���6��4��D!5ל�����QUXz@�;��~T7�˺ɧZ0�K?5��&P�rM�<<禪K�����-�A��k� S�jr+�U;!�D�"䔿z6�.�-w( ������1��p#YYY�?lRBE�T���f4ւsA5��e`�LX�C0�V��{~�(���,�Y5]�[(�RN���dk�$Őz�=�y��v=3��57���;N�L��1za�;����LX�X6�FOS`��cU���\�ؽV�K�c�YB�o���R+��D�$�I���"�=����NaAie)�]~>�b�$/����d�y�t Ȏv	R�U4�K=��7��[������3�����v�!�8��p��gh��^��#YYY=�E�#�Vvt��Kb�8y��y��Eγ��t4+��<~M��;�����u:�x.��C�xI�2(O-kG2��D���@����X�4�����{O�4m�IxW��QTLL:0���'�K�Uz������#YYY�	�������B� 0�ff1�8I��Ml�M$)���f!�s��fBh9yW�^��#YYY��NgV��Wc�ۊ�%��������a�dX��Bu6�##�� n5�w,�W�j3�c�V����������0�����H���Z���S� ���`D�YBY��#APY�)�@� n�MM>���j7�:Y.3;v�`@5�����E:&ش2�~�<F���3o���i��V���)�ٱa�p~f�Vh�)�C�h�]�1��$��ŉ���Q	�LєlQ4��|���h�JS��y[$i�O%��f V��U$��9K�I(w ��)J�#��U)<�7�M���#XXX W6��{#A��Y��Eva��Ø��i�a�1�Q;i��1��M��u�!쾊`Fc�þ�~��tݽMx!Ac�@���Zb����1��E��sq��6�U���@�On��*�P����k-I�m�Њ\������@ڇ1ˡ��#YYY�t�Ғl���'��� �7X��,L%.J�r�j��#YYY��#XXX�xY�}{��dW?m�⊵vJțxҺ�YL0��Yz�l+��Vq�[,�-� �_Gf{>�ُ}�� ���V�M&,��J#���+��y���}v�H���$K�E�Y��#XXX�9|�#X]8|С��Tx�2�Y���g�2�Ks]�{b�U#YYY�����c�@RL�"@�C���s����g�|@�@�����e�wt�: �$����0䦆 ,p�'}&�hOB+g��wmiT�jC�TD��Łk�ŨdR3��nM*�n��ـ$$#XXX��!.�XJ� L�s���'�	 �!@=���3�� �`�'���F���� b1cS���� g,v�`P �,$p_Ux���5��(�T����)�>�x!��I(�	r�H�([{h��`��q����LF`�T�A-B�1afJ9}�4�٬���B6Y�����mx�06��P�lx��D·:����SI�<����\1Ƨp��D�:X�Y:]�Gl���*�9�&٪��ǡ��]#XXX�|&.:���{~<y9U��]!�V�;�^�����Q�kI���A�M������B��k��ŵ#XXX��Uv��ڨ����=b�#XXXāP_p�j�{AQ�Í1q��s�l{�7���饃�b�:�ΐ(�xrok�K�h2�M4��9������#S%�%H�}�v��rZK����Ic�<�#YYY���ګO�ZCc�3-�uz�ꑤf(*�D�`sG��#YYYu�#��$Bb���ѹ+[{��M�,�c��o.u�C[NX�I#YYYx��Ҧ���\)|0�ʪ�.�o�J\L@�!�3�p�]dɤ��!"���]����î�#䛾yV�|��(�*Г|��]iT��sCavq�p#XXX���#XXX#�U� u�F$q�H��ނa���b���e��vm4�S��9J�4�^>XM������T��<�x�RT<��`/$R*���xG+�mk4o�d7/��;OD(�$���Yc��#YYY�Ff�>n�<EP�8�V#XXX� �+�M����4��SY]\�����������2�����3VDR����D6��Q�P:�������#YYY�s<��#YYY%����~g�Yy�=�ޮ5_��~���q��$�ʃ�h$��SL���N:v��?wG2�$"I;X��y����=�?Y�0{�Mcя��}���ό@$d����_n���^�,h�����30̈T�� nd�g��	"R��#4���jԹ��'�+�G�A��0�뉶Zv����A�%������b�h^���&��$擤PZLܟ^�W^G<F��Q�3�F@󲢘��R��N���o��4P9(A+�0��'T��湇ߕ�پ�Z�l��&F	�X���\>7]^����#YYY�\��D(�z��l9������֖1~oDI$�����\�2�v���z��f���J�D_�byӚU�'6����,�TռA#�8�u;Ʈx��/-�`���F��ۊ�n,"@iZb��'��o�:f�:ب�{���[����`ti�X5H�,B@���$%p�2�����̙Q���AȈ��^j��5���M �W,��Y�J���r��4����R�c'��S��0���x沱3�&���e�S*�WAP����$,H"o0#XXXoM��Kȗ��� &#YYY�q6J�`U#YYY�5��]~쩎6pUcA���?G�#XXX�\/�������Mߪb� �?f9��Α�>�߲Z��eu LD<�t��?��/�>HW�2�	>�>(�������!^$q,�ێ�$�}��\XA��YCQ�4Ga��K ��3�:%�6S#YYY8d��a�C�Ek�k'e���B���%+�C,I5�x�{:���)�ʺ 5#XXXd�#XXXw@�"��=�֥����:��<>n��V!_#XXX)V���_{�΢J��$p#�O���m�I�:dW��k�mQ̞���w2#XXXnJ��)�<�E��%E���.���x���2{$��h�ȇ����*j����v��#YYYJV���C����B��������}ius�q t7o&�.s�������#YYYI1�j�{�{��j6s���>��#YYY��>�GxyQK+�ɨ�@�w�8��$bn��{�N_!�hI�VEZV<9��MJb\A*T�e֐��+E��62窈�����g�"$�3f`y�]�Ο��#@�ױW�4��`��)��V#YYY��y��e�������=�.0#YYY}J����䐸��M�����ED|��C��3;�foS���D��d�0���Hd���:�rWSU�.@�E-A�i1%ԗf�.�c߆�nR�Ϗ�: 7F#��� L���dJJA��z�� D$@�P#�x�?��;�����	���9��V�U���V7M��/�GI;ULQRUUHE\���yq����ҝ��NU�ұ"#XXX���0�Þ,��$V�T��Z��A����(7�#XXXOuсb���K���pB���������~]B�(��J�QǄS� �]w셉r��B��T�f)(�Ro���\퀶�Æ����cE���W����uz�b�rdS7B�����~xZ�yF�����UF�ǻuͶ��f�d	7g�j��2u���#�	-OEE=�ĮTIL�h�	��y���#XXX�;�JG���� ��E4R�`�2��_R�jT겶��y��\\W��qAӯ�?����uRX��C���Of��.���L%	JV��K"��%i�C��NFp����чWQ�Xs��!x�dt��} w���y����1� )�ҘB,�Um��?���n��u��b���T#YYY���x"�|@�q���� �򛾳_ s�(�m0�_�-������)�@��!n���S��q8���AN��ω%�G���.�����!gaX�C(���WXX�e,����w����8G@_)*�B���h"Z��a�����^!� �]�=F	�ٚ���B����?ZM�ꦢ#2�!YH`1IL�fbV�����tAN�Ĉ���(�XKUR��x����`��4_;q�b	����C��D4DR�$K�_��⼪���^�59%	gE��T�oHuD9Qw�#щ���ya��A�b����s fܳM*�pD��1�y��=V�#YYY�ju�M/#UE0����=��Xh}��(�������˽"Y��IeA-'e�(22j*S��,A�k��z�%��f)h6�B��f#��a�ԝ&R�Kv�x��.����r#YYYPf�� ƛ�ڞ�s�bpn�+�M����\�B`�&�:�Aa���C�x���=�*;�<�N��3Y����,r�Ģ8#zɝϲ&򜮖Z�(e���ũ0(�#�Ĉ�c#XXX�Rc�Aչ�a��}x���u �IA��VR�v�`a|!uuJ_�%�>/���C��+Ӹ"(_Ç���dSTy���#XXXw���q��9��YTf�0��@��g�arsq���7��M!�p!�Sk(���#YYY}qE��#YYYmw��h�)�던�2�$��$	$m܉�:�$�)bt)!|�]�Zŉ�Ġ"�4�C��}'�!!@��a=�_GA�}�wA�H�;��?�2#XXX�o���u��f�#YYY٨֪J�9��{N ؚ1DS�<��a�ڊ!�P&FFw'Z��͈�q�t=#YYY3�H��|JR�__��A�������r�d��}�:rcJW6Q��"f=<A8Ƙ?d	����<Yݪ̦���_#YYY�A�7h+�ޏȑ��z���w�3����6n����T��1&1��2��"�@�@�G#XXXg#��Y�1��ϥ�O>*9���?�2APq���ý����	�-�8a��Z�I�f7�N���!��9sE�g0�F�$�a��XP�G�r>)����?_��Z�i�q�Ŗ��ВP�0@X����c��=��뵛'��v�����L��#&i'������k�Ӏ�Ds��aLm�F2�P����p��7��S�Z3)*X$22�J^�z7�|m�L}�RNQ*Z�T��f��U{�s���kC	�7U��zw\�:�/{�C�!���������է�n��	P'M"?åNHm�K����7'>nɩ ;����i�5;嗽5��_x����Px��y�7�Lԃ�+��`H6Д ��Xmi%"A��	�o{�	4�fA������E0+fB�$Vd��8�m����޶V�;�A�'�7�����ѽ�o6��ҀЈ�#u+�`Ǒ�O ��i!�ff���Y`A~y��M*�1�k��D�5�m�Jm79�G�-e�\u�6�Y�����ܬ1���i�o7�U#[`I��\�f��0�F�G����� ��{#����4�Q��5f�E�ٞ��5-�X$ƃhhf�142E�'�&��1�&�}&�#VP�^tij����p��Qd��:�!�'�w�wR��\��F���8�DaZ�`�2�*0rcxAV6�`��B�vZ��6�;#Z6iۃ�2���V�X`��f"���a�Zi�"MG�q^����U0P�]?�}��^}�(�/x�8!�G�>>x\���`�♴%C�K��ǔ��q^�mM'��/����>�(]��,h�Y�J��k�']����k�IV.~��M�%����v��닐�F�\8g-��#XXX����Z�~���F3V�;��g/p);d�|�(\��?�:�cv{ܘ�:32G۬A�IM? dN��P�8��I�e �:��`�&q�1`GI+���E'�Z��H^���Oe���*�����1������ �#YYYw+�wG�.(�b��������L1�A�#�r�gD�F��5�;�$^P�S���W@oDz�q�SI�_�O��<p��#XXXP�h#XXX��40��a�z��g١��h|_�)�ȘC�E�!KHL`�j#L,*� �$�B� h������*�;1����ߍL?�1#ôB��4��"�˘Ω���H��QZ)-YZ�`�pl�;�C~�ߜ�&2(��c�X�*��Pd�L�SJup�3#XXX�b���_QJL��4���Y�/U���/��e˒v��Q��%#XXXD�QD�N}]G «��ņQ�N���;�h��Pkh@�;;p-`��9��a͢)�I�0FaP	,C����)HRj��K$\H��P��L�;��16y'hvt7�4G7 �)���{k�A�WWFU�lE����H��j��BQ<�8H��6lv�㓺���-V�r]h%#�l�RҐfƩ�~9�mT�G-F�ZS�U����bW����RkW����~"({��҇D��<P�?�T�����q�us�T�%ģ��dwOК`��E�u?��+[l����J"���V��ڔ����)B�2;K�v��ᕠ >���Ph��Ƶ���)�2 ��ަF4d	�&�W��d�t!Zֿb�~�N�����#�#��Cd	-.� �m��`-��8?>C�������r��K�{/s�ΘZ�FA�����#XXXMN 3�����/�#XXX.C]��/B/�u�!}��}���$��l`lG=�q�@9&`lT�S����mRUUT�a��G<��^^|S�8bc4(Tu˯7�Ȧ[�ct.�Z[_M�5Cp�)Ͻ_9��ce���]�E<���������>��f�P�>�=֝8#XXX{Dd<��"���6>}!�e<�D����$��y����^�X�I��i�����߲& �)#XXXH� �V%AQ�D�SDܬ+67X�UJÒ�bĬ5�#XXXU�D����,J@��m~F��#YYY�h�Ȓ�d�	�� A��Jd�2�#YYYPK2���L��եh�e@L%M4Dq�5-#XXXn%�^�z�@И��C��كF)�N��jJ"���UJ�#$�z��3��S;3�L��Q4K��f�X�Me����JC�s��4DP�R	�cK�O�$�S�C��r��<�8ơ�;$�$ ȇ�8au%�w�q��"Cz�ӥU�tB6��:�n$ږ!��;�+l�ZeМ$��P��V>��N�s�>)	D�I�W��ƻ�-V��Q�iB���#XXX�Ÿ7�u�)����CXs�R�5�m��a�E�3-��TipS�K�n�H�Z�!Kn��3/^��^���U:�W����z���� �2�A�TLlɆL�b" �	�1��܍;i)��Wt�͛c�U��H�-#�S�ƥ�g�6!2�c�w�h��Jr����W�qЮ�H:H��@1=�՘��;%+F�]*���4��E;�p�^�潷��7���)��iD#XXX ���# �.��؛A2*H#XXX��%�=��L�>?��Du�Z�wA�;ң�zI*���#XXX}��Y��k3+�?Ae�AH�(P=���X{}��?|�3�����՝���i|�!�3�q��p�'O��='����wK~o	�.BAAl�84�o�l�2ۼ;C�"eDw���`�d�Df��{Qd���R�� ��X���z���ӄ�Y� 3.RV�',�-F�^}��� Pi��)��5����i2`\DBe�s&���14Z�#XXXQ�<E�(��&�!6��}����1���U-b%u��7!ZOF@�#��݂"	k�/@�B��ɂ[{�èHh;Q�k���&qPuY��s�eYw}���Xc����k�6ΞUmЇ- ��jD�0�!B��ƯX=�#KJ�n�p(v�6mq#XXX#XXX�AH�7��W��m��I�;��in����Q�	�c;I��G�:��0�|�OVV���f����86}rb�t�ϒ}��a��\��=�h�\�ir�,��z���<MA�i뫴U�K�"@������R-y}N��`.8�N �\ih��Q��P#XXX��'X�k��g!�}�>Е�n�K���yIp������[����^h��r#YYY�2` ��>�&�X���C�f��6|���Ϣx��LH�l|KB64�}��2z��װ���$S>�X6m/�$�$w�zV��Jv��� 	`"�b�bh�f�ϝzXY�7��������Q��S>!�˂��JD`��yr�?.}���OwvU	*$��ʽ:3Fh� ϰr�7����5�qi�!])�i���v�B� �="�ְ0�9����v���|,gA��x9b�̆1�J����4H�cp���Ҹ�!��*���_D�{W���႐�i�R����Fd�|6T������潧�>b[�i��E9~K�{�l8C�����w�*B���� �?n�_n��}����:����KS �N��2��ࢎ��v�h:�����<�ڟ?d}�D�),��2'q5}�ݼ���_=&uٲ�^�-f{���&1ӝ�@ľB��v{;8xv)�C�MJ�KBM�,h��BB��	��RA�2�f�g��`U��&�P[�ciq� Ԗc�#YYYAJi�#XXX`.�+���H�-�NY���@j"�)Xc�|��.rD8�x�H����� �v�96g��.𙩦�����h�h�Yf����0��$�L���iP�ev�݈tqt<�{x�vѡ�,U�EO���`H/��<H�����p���sRX=����1#�7�C˨Ajx��|��C�d@����R8����c��\�Ai��K;t;��d]!��DL�'������Y L;�+��w$����\�(7�|hM���lf��X8�gU$,��;�ߎd���A�&]U�����k�#YYY�v��ȗx��M��D$��z��H��]I����&ﵽK�D��Y��S(7J�B��W�~��|��rf4rd����9���(�&\��qw2�=6A���7�,Y��L�;_39ˏV�Ӌ�>k�Z�xŦ�k��c(�׮�{o���xP����X.+w��NMc#XXXHħ�мZe�`��xdL*��ήwjYFk�b��YN,T;�*�[����u�lJ��7��R(�j�w���p�q�ܠ�i��t;q�� �#YYYʶi���TT��tX�SD��Ń`n�hE:��`�0lhf���#YYYUBh��d�1|^D����B� F!�Gw�Y�jiX�TUaי�����lM�9�}�	�8;}kn_���,m�_���vk��W�sD�@?�:�bc���F��T��gز�Z�0�x*�d�{�8���CO�}��S���<���/�%� ��|D���#�c:���n13��`�3&���v6�0��sx�� \��f��ص6i�Xi�酝2��F)�����/E���H^����$#k��^P��| U���X��9�`T�Ih�3�M��pぇ�R<�I^HUD :�x�W'��@��1�ޠ)��Yʣ�"|eL�-��w=�y�!-|Wk:��T�*	��Sr��L�|e�� 22Q��xH���C ܔ<�'����qݧ�aB?�"�=�d�3�����t�2v�0I�'ӯ=<<@ϧ���˦���s�$E��oa!li� �o]�`ҎA�IA���!�+"R��M�H�@WwaX7���#YYY#����I#;�e6;�ڢ��a	ȫJ�(�e����FHR��zY�Pg�eX���~]��$b7�R��P��pp�#��I�"���(K��ER�j���c�� /�����,��[��>n���x�" �NL�a�������x0��}�� Id* Ci��s����EۄE�j��$�Y�S�r�];��D0H���F0k{���7�t���څ����{�tU<�SD�J�(`^�~�eUT�.L�1�$��k�*^Q!Wz3�~+-���A�譁����5�f`Je��M �� ���:���0��v~�>�� ��=��A�9�jY(@�/oB��y�b�g���L �#YYY�4$/\U[d��R�/�S#XXXn6ͥ��W=��E)� qҰ�z���	=��kg[0�>�=(��vҧL$jo�~rP��	�������#XXX~���FBLO\N�&Q �7��y��:���H����d	����s�rnLA˨�c�iHP�b���2;Ϗ_���9x%���u0 \�R�XSa/+�s�))��Y��Z�C�T�*P�0�re���6?la˯�FDF�_j<��jH�7MNI��q&rΉ�<�\c�A�"���XkJ��)�?@�.ߛo��:��-ד�ˈ&ip�#��kڙI#XXX����##XXX,�l8�:Y����x�C�@t�g�(|�>���N�Jv�*{s�}.;%���hҜ��Z�VjmZS��&�4�e�h�2��=�=Qmx�:j�7p"�}\�RW���,#YYY k� c�������< 6��	��<y��S���Oeszj��c�K�N��e����������&�i�|2��3�����Β�/"�K��6ԽH�~���r"�cl���L�^��w�N�F�J�1�W��'=��f��6Phd�!��ɂ��k5����&�� �-cG/��$bi�� ��b�U��/T�!Q�YYB�N��]���#XXX)S撼���r�lIQ���%�y ��2>���|a\��|�o�u�m�c�����56$?|$-!6��$��}�?3��������W�i_����p��)�� c�
#<==
